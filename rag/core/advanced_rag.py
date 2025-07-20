#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
進階RAG系統 - 整合真實語言模型和向量資料庫
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import asyncio

# 條件性導入，支援多種配置
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    HAS_VECTOR_DB = True
except ImportError:
    HAS_VECTOR_DB = False

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB_SCRAPING = True
except ImportError:
    HAS_WEB_SCRAPING = False

logger = logging.getLogger(__name__)

class AdvancedRAGSystem:
    """進階RAG系統 - 整合真實語言模型"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化RAG系統
        
        Args:
            config: 配置字典，包含API keys和模型設定
        """
        self.config = config or {}
        self.vector_store = None
        self.embedding_model = None
        self.knowledge_base = []
        self.initialized = False
        
        # 設定API keys
        self._setup_api_keys()
        
        # 初始化向量資料庫
        self._initialize_vector_store()
        
        # 初始化嵌入模型
        self._initialize_embedding_model()
        
        # 載入知識庫
        self._load_knowledge_base()
        
        self.initialized = True
        logger.info("進階RAG系統初始化完成")
    
    def _setup_api_keys(self):
        """設定API keys"""
        # 從環境變數或配置文件載入
        if HAS_OPENAI:
            openai_key = (
                self.config.get('openai_api_key') or 
                os.getenv('OPENAI_API_KEY')
            )
            if openai_key:
                openai.api_key = openai_key
                self.has_openai = True
                logger.info("OpenAI API key 已設定")
            else:
                self.has_openai = False
                logger.warning("未找到 OpenAI API key")
        else:
            self.has_openai = False
    
    def _initialize_vector_store(self):
        """初始化向量資料庫"""
        if HAS_VECTOR_DB:
            # 使用FAISS作為向量資料庫
            self.dimension = 384  # sentence-transformers 預設維度
            self.vector_store = faiss.IndexFlatIP(self.dimension)  # 內積相似度
            self.document_metadata = []
            logger.info("FAISS向量資料庫初始化完成")
        else:
            logger.warning("未安裝向量資料庫依賴，將使用簡化版本")
    
    def _initialize_embedding_model(self):
        """初始化嵌入模型"""
        if HAS_VECTOR_DB:
            try:
                # 使用多語言模型，支援中文
                model_name = self.config.get(
                    'embedding_model', 
                    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
                )
                self.embedding_model = SentenceTransformer(model_name)
                logger.info(f"嵌入模型 {model_name} 載入完成")
            except Exception as e:
                logger.error(f"載入嵌入模型失敗: {e}")
                self.embedding_model = None
        else:
            logger.warning("未安裝sentence-transformers，將使用關鍵詞匹配")
    
    def _load_knowledge_base(self):
        """載入知識庫"""
        # 從文件載入
        knowledge_file = Path("data/knowledge_base.json")
        if knowledge_file.exists():
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
                logger.info(f"從文件載入了 {len(self.knowledge_base)} 條知識")
        else:
            # 使用預設知識庫
            self.knowledge_base = self._get_default_knowledge()
            logger.info(f"使用預設知識庫，共 {len(self.knowledge_base)} 條")
        
        # 建立向量索引
        if self.embedding_model and self.vector_store:
            self._build_vector_index()
    
    def _get_default_knowledge(self) -> List[Dict[str, Any]]:
        """獲取預設知識庫"""
        return [
            {
                "id": "finance_001",
                "title": "股票投資基礎",
                "content": "股票投資是購買公司股份的行為，投資者成為公司的部分所有者。投資股票的主要目的是獲得資本增值和股息收入。在投資前，應該了解公司的基本面、財務狀況、行業前景等因素。",
                "category": "投資教學",
                "source": "財經教學"
            },
            {
                "id": "finance_002", 
                "title": "技術分析簡介",
                "content": "技術分析是通過研究股價走勢圖表來預測未來價格變動的方法。常用的技術指標包括移動平均線、相對強弱指數(RSI)、MACD等。技術分析假設股價已經反映了所有相關信息。",
                "category": "技術分析",
                "source": "投資指南"
            },
            {
                "id": "finance_003",
                "title": "風險管理",
                "content": "投資風險管理是保護投資組合免受重大損失的策略。包括資產分散化、設定停損點、位置控制、定期再平衡等。好的風險管理能幫助投資者在市場波動中保持穩定的長期回報。",
                "category": "風險管理",
                "source": "投資策略"
            }
        ]
    
    def _build_vector_index(self):
        """建立向量索引"""
        if not (self.embedding_model and self.vector_store):
            return
            
        try:
            # 提取文本內容
            texts = []
            for doc in self.knowledge_base:
                text = f"{doc['title']} {doc['content']}"
                texts.append(text)
            
            # 生成嵌入向量
            embeddings = self.embedding_model.encode(texts)
            embeddings = np.array(embeddings).astype('float32')
            
            # 正規化向量（用於內積相似度）
            faiss.normalize_L2(embeddings)
            
            # 添加到向量資料庫
            self.vector_store.add(embeddings)
            
            # 保存元數據
            self.document_metadata = self.knowledge_base.copy()
            
            logger.info(f"向量索引建立完成，共 {len(texts)} 個文檔")
            
        except Exception as e:
            logger.error(f"建立向量索引失敗: {e}")
    
    def add_knowledge(self, documents: List[Dict[str, Any]]):
        """添加新知識到知識庫"""
        for doc in documents:
            # 確保文檔有必要字段
            if 'id' not in doc:
                doc['id'] = f"doc_{len(self.knowledge_base)}"
            if 'timestamp' not in doc:
                doc['timestamp'] = datetime.now().isoformat()
            
            self.knowledge_base.append(doc)
        
        # 重建向量索引
        if self.embedding_model and self.vector_store:
            self._build_vector_index()
        
        logger.info(f"添加了 {len(documents)} 條新知識")
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """檢索相關文檔"""
        if self.embedding_model and self.vector_store and self.vector_store.ntotal > 0:
            return self._vector_retrieve(query, top_k)
        else:
            return self._keyword_retrieve(query, top_k)
    
    def _vector_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """使用向量檢索"""
        try:
            # 生成查詢向量
            query_embedding = self.embedding_model.encode([query])
            query_embedding = np.array(query_embedding).astype('float32')
            faiss.normalize_L2(query_embedding)
            
            # 搜索相似文檔
            scores, indices = self.vector_store.search(query_embedding, top_k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx >= 0 and idx < len(self.document_metadata):
                    doc = self.document_metadata[idx].copy()
                    doc['similarity_score'] = float(score)
                    doc['rank'] = i + 1
                    results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"向量檢索失敗: {e}")
            return self._keyword_retrieve(query, top_k)
    
    def _keyword_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """關鍵詞檢索（後備方案）"""
        results = []
        query_lower = query.lower()
        
        for doc in self.knowledge_base:
            content = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            
            # 計算關鍵詞匹配分數
            score = 0
            for word in query_lower.split():
                if word in content:
                    score += content.count(word)
            
            if score > 0:
                doc_copy = doc.copy()
                doc_copy['similarity_score'] = score / len(query_lower.split())
                results.append(doc_copy)
        
        # 排序並返回前top_k個
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:top_k]
    
    async def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """生成回答"""
        if self.has_openai:
            return await self._openai_generate(query, context_docs)
        else:
            return self._template_generate(query, context_docs)
    
    async def _openai_generate(self, query: str, context_docs: List[Dict]) -> str:
        """使用OpenAI生成回答"""
        try:
            # 構建上下文
            context = "\n\n".join([
                f"文檔標題: {doc['title']}\n內容: {doc['content']}"
                for doc in context_docs
            ])
            
            # 構建提示詞
            prompt = f"""
基於以下上下文信息，請回答用戶的問題。如果上下文中沒有相關信息，請誠實說明。

上下文:
{context}

用戶問題: {query}

請用繁體中文回答，並盡量簡潔明了：
"""
            
            # 調用OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的財經顧問，專門回答股票投資相關問題。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI生成回答失敗: {e}")
            return self._template_generate(query, context_docs)
    
    def _template_generate(self, query: str, context_docs: List[Dict]) -> str:
        """使用模板生成回答（後備方案）"""
        if not context_docs:
            return "抱歉，我沒有找到相關的資訊來回答您的問題。"
        
        # 使用最相關的文檔
        best_doc = context_docs[0]
        
        # 簡單的模板回答
        response = f"根據我的了解，{best_doc['content']}"
        
        # 如果有多個相關文檔，提及其他信息
        if len(context_docs) > 1:
            response += f"\n\n另外，{context_docs[1]['title']}也值得了解。"
        
        return response
    
    async def query(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        查詢RAG系統
        
        Args:
            message: 用戶查詢
            context: 對話上下文
            
        Returns:
            包含回答、來源和信心度的字典
        """
        try:
            # 1. 向量檢索相關文檔
            relevant_docs = await self._retrieve_documents(message)
            
            # 2. 生成回答
            if self.has_openai and relevant_docs:
                # 使用 OpenAI 生成高品質回答
                answer = await self._generate_with_openai(message, relevant_docs, context)
                method = "openai_rag"
                confidence = 0.9
            else:
                # 使用模板生成回答
                answer = self._generate_with_template(message, relevant_docs)
                method = "template_rag"
                confidence = 0.7 if relevant_docs else 0.3
            
            return {
                "answer": answer,
                "sources": relevant_docs[:3],  # 前3個最相關的來源
                "confidence": confidence,
                "method": method,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"RAG查詢失敗: {e}")
            return {
                "answer": f"抱歉，查詢時發生錯誤：{str(e)}",
                "sources": [],
                "confidence": 0.0,
                "method": "error",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _retrieve_documents(self, query: str) -> List[Dict[str, Any]]:
        """檢索相關文檔"""
        if not (self.embedding_model and self.vector_store):
            return []
        
        try:
            # 生成查詢向量
            query_vector = self.embedding_model.encode([query])
            query_vector = np.array(query_vector).astype('float32')
            faiss.normalize_L2(query_vector)
            
            # 搜索最相關的文檔
            top_k = self.config.get('top_k_retrieve', 3)
            scores, indices = self.vector_store.search(query_vector, top_k)
            
            # 構建結果
            results = []
            confidence_threshold = self.config.get('confidence_threshold', 0.3)
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if score > confidence_threshold and idx < len(self.document_metadata):
                    doc = self.document_metadata[idx].copy()
                    doc['score'] = float(score)
                    doc['rank'] = i + 1
                    results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"文檔檢索失敗: {e}")
            return []
    
    async def _generate_with_openai(self, query: str, docs: List[Dict], context: Optional[Dict] = None) -> str:
        """使用 OpenAI 生成回答"""
        try:
            import openai
            
            # 構建上下文
            doc_context = "\n\n".join([
                f"來源 {i+1}：{doc['title']}\n{doc['content']}"
                for i, doc in enumerate(docs[:3])
            ])
            
            # 系統提示
            system_prompt = self.config.get(
                'system_prompt',
                "你是一個專業的台股財經助手，請根據提供的知識庫內容回答用戶的投資和財經相關問題。"
            )
            
            # 構建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""
根據以下知識庫內容回答問題：

{doc_context}

問題：{query}

請提供準確、專業且易懂的回答。如果知識庫內容不足以回答問題，請說明。
"""}
            ]
            
            # 調用 OpenAI API（新版本）
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=openai.api_key)
            
            response = await client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=self.config.get('max_tokens', 500),
                temperature=self.config.get('temperature', 0.7)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI 生成失敗: {e}")
            # 回退到模板生成
            return self._generate_with_template(query, docs)
    
    def _generate_with_template(self, query: str, docs: List[Dict]) -> str:
        """使用模板生成回答（無需 API key）"""
        if not docs:
            return "抱歉，我在知識庫中找不到相關資訊來回答您的問題。請嘗試提出其他財經相關問題。"
        
        # 找到最相關的文檔
        best_doc = docs[0]
        
        # 根據查詢類型選擇模板
        if any(keyword in query for keyword in ['什麼是', '是什麼', '定義', '意思']):
            return f"根據我的了解，{best_doc['content']}"
        elif any(keyword in query for keyword in ['如何', '怎麼', '方法', '步驟']):
            return f"關於您的問題，{best_doc['content']}\n\n您可以參考以上資訊來了解具體做法。"
        elif any(keyword in query for keyword in ['為什麼', '原因', '影響']):
            return f"這個問題的相關說明是：{best_doc['content']}"
        else:
            return f"根據知識庫資料：{best_doc['content']}\n\n希望這個資訊對您有幫助。"
    
    def _calculate_confidence(self, context_docs: List[Dict]) -> float:
        """計算回答信心度"""
        if not context_docs:
            return 0.0
        
        # 基於最高相似度分數
        max_score = max(doc.get('similarity_score', 0) for doc in context_docs)
        
        # 正規化到0-1範圍
        if self.embedding_model:
            # 向量相似度已經在0-1範圍
            return min(max_score, 1.0)
        else:
            # 關鍵詞匹配分數需要正規化
            return min(max_score / 5.0, 1.0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取系統統計信息"""
        return {
            "knowledge_base_size": len(self.knowledge_base),
            "has_vector_db": HAS_VECTOR_DB and self.vector_store is not None,
            "has_openai": self.has_openai,
            "has_embedding_model": self.embedding_model is not None,
            "vector_store_size": self.vector_store.ntotal if self.vector_store else 0,
            "embedding_dimension": self.dimension if HAS_VECTOR_DB else None
        }

# 網路資料收集器
class WebKnowledgeCollector:
    """網路知識收集器"""
    
    def __init__(self):
        self.has_web_scraping = HAS_WEB_SCRAPING
    
    async def collect_stock_news(self, stock_code: str = None) -> List[Dict[str, Any]]:
        """收集股票新聞"""
        if not self.has_web_scraping:
            logger.warning("未安裝網頁爬蟲依賴")
            return []
        
        try:
            # 示例：從公開API或網站收集新聞
            # 這裡需要根據實際的新聞來源實現
            url = "https://tw.stock.yahoo.com/news"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # 解析新聞內容
                # 這是示例代碼，需要根據實際網站結構調整
                news_items = []
                
                return news_items
            
        except Exception as e:
            logger.error(f"收集股票新聞失敗: {e}")
        
        return []
    
    async def collect_financial_data(self) -> List[Dict[str, Any]]:
        """收集財經資料"""
        # 實現從各種財經資料源收集信息
        return []

# 配置管理器
class RAGConfig:
    """RAG配置管理器"""
    
    @staticmethod
    def load_config(config_file: str = "config/rag_config.json") -> Dict[str, Any]:
        """載入配置文件"""
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return RAGConfig.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """獲取預設配置"""
        return {
            "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "vector_db_type": "faiss",
            "openai_model": "gpt-3.5-turbo",
            "max_tokens": 500,
            "temperature": 0.7,
            "top_k_retrieve": 3,
            "confidence_threshold": 0.3
        }
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_file: str = "config/rag_config.json"):
        """保存配置文件"""
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2) 