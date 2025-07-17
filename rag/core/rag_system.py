#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG (Retrieval-Augmented Generation) 系統
用於增強聊天機器人的知識檢索和回答生成能力
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
from pathlib import Path

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    """RAG系統主類"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """初始化RAG系統"""
        self.config = config or self._get_default_config()
        self.knowledge_base = KnowledgeBase(self.config.get('knowledge_base', {}))
        self.vector_store = VectorStore(self.config.get('vector_store', {}))
        self.embedding_service = EmbeddingService(self.config.get('embedding', {}))
        self.retriever = Retriever(self.vector_store, self.embedding_service)
        self.generator = ResponseGenerator(self.config.get('generator', {}))
        
        # 初始化系統
        self._initialize_system()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """獲取預設配置"""
        return {
            'knowledge_base': {
                'data_dir': 'data/knowledge',
                'cache_dir': 'cache/knowledge'
            },
            'vector_store': {
                'dimension': 384,  # 使用sentence-transformers的預設維度
                'index_type': 'faiss',
                'storage_path': 'cache/vector_store'
            },
            'embedding': {
                'model_name': 'sentence-transformers/all-MiniLM-L6-v2',
                'device': 'cpu',
                'batch_size': 32
            },
            'generator': {
                'model_type': 'local',  # 'openai' 或 'local'
                'max_context_length': 2000,
                'temperature': 0.7
            },
            'retrieval': {
                'top_k': 5,
                'similarity_threshold': 0.5
            }
        }
    
    def _initialize_system(self):
        """初始化系統組件"""
        try:
            # 創建必要的目錄
            for path in [
                self.config['knowledge_base']['data_dir'],
                self.config['knowledge_base']['cache_dir'],
                self.config['vector_store']['storage_path']
            ]:
                Path(path).mkdir(parents=True, exist_ok=True)
            
            # 載入或初始化向量存儲
            self.vector_store.load_or_initialize()
            
            logger.info("RAG系統初始化完成")
        except Exception as e:
            logger.error(f"RAG系統初始化失敗: {e}")
            raise
    
    def query(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """處理查詢並返回增強回答"""
        try:
            # 檢索相關文檔
            retrieved_docs = self.retriever.retrieve(question, 
                                                   top_k=self.config['retrieval']['top_k'])
            
            # 生成回答
            response = self.generator.generate_response(
                question=question,
                retrieved_docs=retrieved_docs,
                context=context
            )
            
            return {
                'answer': response['answer'],
                'sources': response.get('sources', []),
                'confidence': response.get('confidence', 0.0),
                'retrieved_docs': retrieved_docs,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"查詢處理失敗: {e}")
            return {
                'answer': f"抱歉，處理您的問題時發生錯誤：{str(e)}",
                'sources': [],
                'confidence': 0.0,
                'retrieved_docs': [],
                'timestamp': datetime.now().isoformat()
            }
    
    def add_knowledge(self, documents: List[Dict[str, Any]]):
        """添加知識到系統中"""
        try:
            # 添加到知識庫
            self.knowledge_base.add_documents(documents)
            
            # 生成嵌入並存儲
            for doc in documents:
                embedding = self.embedding_service.embed_text(doc['content'])
                self.vector_store.add_document(doc, embedding)
            
            logger.info(f"成功添加 {len(documents)} 個文檔到知識庫")
            
        except Exception as e:
            logger.error(f"添加知識失敗: {e}")
            raise
    
    def update_knowledge_base(self):
        """更新知識庫（從外部資源）"""
        try:
            # 這裡可以實現從各種來源更新知識庫的邏輯
            # 例如：爬取財經新聞、更新股票資料等
            logger.info("知識庫更新功能待實現")
            
        except Exception as e:
            logger.error(f"更新知識庫失敗: {e}")


class KnowledgeBase:
    """知識庫管理類"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_dir = Path(config['data_dir'])
        self.cache_dir = Path(config['cache_dir'])
        self.documents = []
        
        # 載入現有文檔
        self._load_documents()
    
    def _load_documents(self):
        """載入現有文檔"""
        try:
            doc_file = self.cache_dir / 'documents.json'
            if doc_file.exists():
                with open(doc_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                logger.info(f"載入了 {len(self.documents)} 個文檔")
        except Exception as e:
            logger.error(f"載入文檔失敗: {e}")
            self.documents = []
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """添加文檔到知識庫"""
        for doc in documents:
            doc['id'] = doc.get('id', f"doc_{len(self.documents)}")
            doc['timestamp'] = doc.get('timestamp', datetime.now().isoformat())
            self.documents.append(doc)
        
        # 保存到文件
        self._save_documents()
    
    def _save_documents(self):
        """保存文檔到文件"""
        try:
            doc_file = self.cache_dir / 'documents.json'
            with open(doc_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存文檔失敗: {e}")
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """根據ID獲取文檔"""
        for doc in self.documents:
            if doc.get('id') == doc_id:
                return doc
        return None
    
    def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """簡單的文本搜索"""
        results = []
        query_lower = query.lower()
        
        for doc in self.documents:
            content = doc.get('content', '').lower()
            title = doc.get('title', '').lower()
            
            if query_lower in content or query_lower in title:
                results.append(doc)
                if len(results) >= limit:
                    break
        
        return results


class VectorStore:
    """向量存儲類"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dimension = config['dimension']
        self.storage_path = Path(config['storage_path'])
        self.index = None
        self.doc_mappings = {}  # 向量索引到文檔的映射
        
    def load_or_initialize(self):
        """載入或初始化向量存儲"""
        try:
            # 嘗試載入現有索引
            if self._load_index():
                logger.info("成功載入現有向量索引")
            else:
                # 初始化新索引
                self._initialize_index()
                logger.info("初始化新的向量索引")
                
        except Exception as e:
            logger.error(f"向量存儲初始化失敗: {e}")
            self._initialize_index()
    
    def _initialize_index(self):
        """初始化向量索引"""
        try:
            import faiss
            self.index = faiss.IndexFlatIP(self.dimension)  # 使用內積相似度
            self.doc_mappings = {}
            logger.info(f"初始化FAISS索引，維度: {self.dimension}")
        except ImportError:
            logger.warning("FAISS未安裝，使用簡單向量存儲")
            self.index = SimpleVectorIndex(self.dimension)
            self.doc_mappings = {}
    
    def _load_index(self) -> bool:
        """載入現有索引"""
        try:
            index_file = self.storage_path / 'index.faiss'
            mapping_file = self.storage_path / 'mappings.pkl'
            
            if index_file.exists() and mapping_file.exists():
                import faiss
                self.index = faiss.read_index(str(index_file))
                
                with open(mapping_file, 'rb') as f:
                    self.doc_mappings = pickle.load(f)
                
                return True
        except Exception as e:
            logger.error(f"載入索引失敗: {e}")
        
        return False
    
    def save_index(self):
        """保存索引到文件"""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            index_file = self.storage_path / 'index.faiss'
            mapping_file = self.storage_path / 'mappings.pkl'
            
            # 保存FAISS索引
            if hasattr(self.index, 'write_index'):
                import faiss
                faiss.write_index(self.index, str(index_file))
            
            # 保存映射
            with open(mapping_file, 'wb') as f:
                pickle.dump(self.doc_mappings, f)
                
            logger.info("向量索引保存成功")
            
        except Exception as e:
            logger.error(f"保存索引失敗: {e}")
    
    def add_document(self, document: Dict[str, Any], embedding: np.ndarray):
        """添加文檔和其嵌入向量"""
        try:
            # 確保嵌入向量的維度正確
            if embedding.shape[0] != self.dimension:
                raise ValueError(f"嵌入向量維度不匹配: {embedding.shape[0]} != {self.dimension}")
            
            # 添加到索引
            vector_id = self.index.ntotal if hasattr(self.index, 'ntotal') else len(self.doc_mappings)
            
            # 重塑向量為2D數組
            embedding_2d = embedding.reshape(1, -1).astype(np.float32)
            self.index.add(embedding_2d)
            
            # 保存文檔映射
            self.doc_mappings[vector_id] = document
            
            # 定期保存索引
            if vector_id % 100 == 0:
                self.save_index()
                
        except Exception as e:
            logger.error(f"添加文檔到向量存儲失敗: {e}")
            raise
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """搜索相似文檔"""
        try:
            # 重塑查詢向量
            query_2d = query_embedding.reshape(1, -1).astype(np.float32)
            
            # 搜索
            if hasattr(self.index, 'search'):
                scores, indices = self.index.search(query_2d, top_k)
                
                results = []
                for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if idx in self.doc_mappings:
                        results.append((self.doc_mappings[idx], float(score)))
                
                return results
            else:
                # 簡單向量搜索的回退方案
                return self.index.search(query_embedding, top_k)
                
        except Exception as e:
            logger.error(f"向量搜索失敗: {e}")
            return []


class SimpleVectorIndex:
    """簡單向量索引（FAISS的回退方案）"""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors = []
        self.ntotal = 0
    
    def add(self, vector: np.ndarray):
        """添加向量"""
        self.vectors.append(vector.flatten())
        self.ntotal += 1
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        """搜索相似向量"""
        if not self.vectors:
            return []
        
        # 計算餘弦相似度
        query_norm = np.linalg.norm(query_vector)
        similarities = []
        
        for i, vector in enumerate(self.vectors):
            similarity = np.dot(query_vector, vector) / (query_norm * np.linalg.norm(vector))
            similarities.append((i, similarity))
        
        # 排序並返回top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


class EmbeddingService:
    """嵌入服務類"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config['model_name']
        self.device = config['device']
        self.batch_size = config['batch_size']
        self.model = None
        
        # 初始化模型
        self._initialize_model()
    
    def _initialize_model(self):
        """初始化嵌入模型"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"成功載入嵌入模型: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers未安裝，使用簡單嵌入")
            self.model = SimpleEmbedding()
        except Exception as e:
            logger.error(f"載入嵌入模型失敗: {e}")
            self.model = SimpleEmbedding()
    
    def embed_text(self, text: str) -> np.ndarray:
        """將文本轉換為嵌入向量"""
        try:
            if hasattr(self.model, 'encode'):
                return self.model.encode(text, convert_to_numpy=True)
            else:
                return self.model.embed(text)
        except Exception as e:
            logger.error(f"文本嵌入失敗: {e}")
            # 返回隨機向量作為回退
            return np.random.random(self.config['dimension'])
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """批量嵌入文本"""
        try:
            if hasattr(self.model, 'encode'):
                return self.model.encode(texts, convert_to_numpy=True, batch_size=self.batch_size)
            else:
                return np.array([self.model.embed(text) for text in texts])
        except Exception as e:
            logger.error(f"批量嵌入失敗: {e}")
            return np.random.random((len(texts), self.config['dimension']))


class SimpleEmbedding:
    """簡單嵌入模型（回退方案）"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
    
    def embed(self, text: str) -> np.ndarray:
        """簡單的文本嵌入（基於字符哈希）"""
        # 這是一個非常簡單的嵌入方法，僅用於演示
        hash_value = hash(text)
        np.random.seed(hash_value % (2**32))
        return np.random.random(self.dimension)


class Retriever:
    """檢索器類"""
    
    def __init__(self, vector_store: VectorStore, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """檢索相關文檔"""
        try:
            # 生成查詢嵌入
            query_embedding = self.embedding_service.embed_text(query)
            
            # 搜索相似文檔
            results = self.vector_store.search(query_embedding, top_k)
            
            # 格式化結果
            retrieved_docs = []
            for doc, score in results:
                retrieved_docs.append({
                    'document': doc,
                    'similarity_score': score,
                    'relevance': 'high' if score > 0.8 else 'medium' if score > 0.5 else 'low'
                })
            
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"檢索失敗: {e}")
            return []


class ResponseGenerator:
    """回答生成器類"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_type = config['model_type']
        self.max_context_length = config['max_context_length']
        self.temperature = config['temperature']
        
        # 初始化生成模型
        self._initialize_generator()
    
    def _initialize_generator(self):
        """初始化生成器"""
        if self.model_type == 'openai':
            self._initialize_openai()
        else:
            self._initialize_local()
    
    def _initialize_openai(self):
        """初始化OpenAI模型"""
        try:
            import openai
            # 這裡需要設置OpenAI API密鑰
            # openai.api_key = "your-api-key"
            logger.info("OpenAI生成器初始化")
        except ImportError:
            logger.warning("OpenAI未安裝，使用本地生成器")
            self._initialize_local()
    
    def _initialize_local(self):
        """初始化本地生成器"""
        logger.info("使用本地模板生成器")
    
    def generate_response(self, question: str, retrieved_docs: List[Dict[str, Any]], 
                         context: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成回答"""
        try:
            if self.model_type == 'openai':
                return self._generate_with_openai(question, retrieved_docs, context)
            else:
                return self._generate_with_template(question, retrieved_docs, context)
        except Exception as e:
            logger.error(f"生成回答失敗: {e}")
            return {
                'answer': f"抱歉，生成回答時發生錯誤：{str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def _generate_with_openai(self, question: str, retrieved_docs: List[Dict[str, Any]], 
                             context: Dict[str, Any] = None) -> Dict[str, Any]:
        """使用OpenAI生成回答"""
        # 構建提示
        prompt = self._build_prompt(question, retrieved_docs, context)
        
        # 這裡實現OpenAI API調用
        # 由於需要API密鑰，暫時使用模板方法
        return self._generate_with_template(question, retrieved_docs, context)
    
    def _generate_with_template(self, question: str, retrieved_docs: List[Dict[str, Any]], 
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """使用模板生成回答"""
        if not retrieved_docs:
            return {
                'answer': "抱歉，我沒有找到相關的資訊來回答您的問題。",
                'sources': [],
                'confidence': 0.0
            }
        
        # 提取最相關的文檔
        best_doc = retrieved_docs[0]['document']
        
        # 構建回答
        answer = f"根據我的知識庫，{best_doc.get('content', '相關資訊暫時無法提供')}"
        
        # 添加來源資訊
        sources = []
        for doc_info in retrieved_docs[:3]:  # 只顯示前3個來源
            doc = doc_info['document']
            sources.append({
                'title': doc.get('title', '未知來源'),
                'content_preview': doc.get('content', '')[:100] + '...',
                'similarity': doc_info['similarity_score']
            })
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': retrieved_docs[0]['similarity_score'] if retrieved_docs else 0.0
        }
    
    def _build_prompt(self, question: str, retrieved_docs: List[Dict[str, Any]], 
                     context: Dict[str, Any] = None) -> str:
        """構建提示模板"""
        prompt = f"""基於以下相關資訊，請回答用戶的問題。

問題：{question}

相關資訊：
"""
        
        for i, doc_info in enumerate(retrieved_docs[:3]):
            doc = doc_info['document']
            prompt += f"\n{i+1}. {doc.get('title', '文檔')}：{doc.get('content', '')}\n"
        
        prompt += "\n請基於上述資訊提供準確、有用的回答。如果資訊不足，請說明。"
        
        return prompt


# 全域RAG系統實例
rag_system = None

def get_rag_system() -> RAGSystem:
    """獲取全域RAG系統實例"""
    global rag_system
    if rag_system is None:
        rag_system = RAGSystem()
    return rag_system

def initialize_rag_system(config: Dict[str, Any] = None):
    """初始化RAG系統"""
    global rag_system
    rag_system = RAGSystem(config)
    return rag_system 