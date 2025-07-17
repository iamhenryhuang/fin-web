#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
輕量級RAG系統 - 整合OpenAI但避免複雜依賴
"""

import os
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class LightweightRAGSystem:
    """輕量級RAG系統 - 使用OpenAI embeddings和GPT"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化輕量級RAG系統"""
        self.config = config or self._load_config()
        self.knowledge_base = []
        self.embeddings_cache = {}
        self.openai_api_key = self.config.get('openai_api_key', '')
        
        # 檢查API key
        if not self.openai_api_key:
            self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        self.has_openai = bool(self.openai_api_key)
        
        # 載入知識庫
        self._load_knowledge_base()
        
        logger.info(f"輕量級RAG系統初始化完成，OpenAI可用: {self.has_openai}")
    
    def _load_config(self) -> Dict[str, Any]:
        """載入配置"""
        config_file = Path("config/rag_config.json")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "openai_model": "gpt-3.5-turbo",
            "embedding_model": "text-embedding-ada-002",
            "max_tokens": 500,
            "temperature": 0.7,
            "top_k_retrieve": 3
        }
    
    def _load_knowledge_base(self):
        """載入知識庫"""
        # 嘗試從文件載入
        knowledge_file = Path("data/knowledge_base.json")
        if knowledge_file.exists():
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            # 使用預設知識庫
            self.knowledge_base = self._get_default_knowledge()
        
        logger.info(f"載入了 {len(self.knowledge_base)} 條知識")
    
    def _get_default_knowledge(self) -> List[Dict[str, Any]]:
        """獲取預設知識庫"""
        return [
            {
                "id": "stock_001",
                "title": "股票投資基礎",
                "content": "股票投資是購買公司股份，成為公司股東的投資方式。投資者可以通過股價上漲獲得資本利得，也可能獲得公司分發的股息。投資前應該了解公司的基本面、財務狀況、行業前景等因素。股票投資具有風險，需要做好資產配置和風險管理。",
                "category": "投資基礎"
            },
            {
                "id": "analysis_001",
                "title": "基本面分析",
                "content": "基本面分析是評估公司內在價值的方法，包括財務報表分析、產業分析、經濟環境分析等。重要的財務指標包括本益比(PE)、股價淨值比(PB)、股東權益報酬率(ROE)、每股盈餘(EPS)等。投資者應該關注公司的營收成長、獲利能力、負債狀況等。",
                "category": "分析方法"
            },
            {
                "id": "analysis_002",
                "title": "技術分析",
                "content": "技術分析是通過研究股價圖表和交易量等市場數據來預測股價走勢的方法。常用的技術指標包括移動平均線(MA)、相對強弱指數(RSI)、隨機指標(KD)、MACD等。技術分析假設股價已經反映了所有相關資訊，過去的價格模式會重複出現。",
                "category": "分析方法"
            },
            {
                "id": "risk_001",
                "title": "投資風險管理",
                "content": "風險管理是投資成功的關鍵要素。主要的風險管理策略包括：資產分散化投資、設定停損點、控制單一部位大小、定期檢視投資組合等。投資者應該根據自己的風險承受能力制定投資策略，不要把所有資金投入單一股票或產業。",
                "category": "風險管理"
            },
            {
                "id": "taiwan_market_001",
                "title": "台股市場特色",
                "content": "台灣股票市場以科技股為主要特色，特別是半導體產業在全球具有重要地位。台積電、聯發科等公司是台股的重要權值股。投資台股需要關注國際科技趨勢、兩岸關係、美中貿易關係、匯率變化等因素。台股市場相對較小，容易受到外資進出影響。",
                "category": "市場分析"
            }
        ]
    
    async def get_embedding(self, text: str) -> List[float]:
        """獲取文本嵌入向量"""
        if not self.has_openai:
            # 如果沒有OpenAI，返回簡單的文本哈希作為特徵
            return [float(hash(text + str(i)) % 1000) / 1000 for i in range(10)]
        
        # 檢查快取
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'input': text,
                'model': self.config.get('embedding_model', 'text-embedding-ada-002')
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.openai.com/v1/embeddings',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        embedding = result['data'][0]['embedding']
                        self.embeddings_cache[text] = embedding
                        return embedding
                    else:
                        logger.error(f"OpenAI embedding API 錯誤: {response.status}")
                        return [0.0] * 1536  # 預設維度
        
        except Exception as e:
            logger.error(f"獲取嵌入向量失敗: {e}")
            return [0.0] * 1536
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """計算餘弦相似度"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = sum(a * a for a in vec1) ** 0.5
        norm_b = sum(b * b for b in vec2) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    async def retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """檢索相關文檔"""
        if self.has_openai:
            return await self._semantic_retrieve(query, top_k)
        else:
            return self._keyword_retrieve(query, top_k)
    
    async def _semantic_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """使用語義相似度檢索"""
        try:
            query_embedding = await self.get_embedding(query)
            
            # 為所有文檔獲取嵌入
            doc_similarities = []
            
            for doc in self.knowledge_base:
                doc_text = f"{doc['title']} {doc['content']}"
                doc_embedding = await self.get_embedding(doc_text)
                similarity = self.cosine_similarity(query_embedding, doc_embedding)
                
                doc_copy = doc.copy()
                doc_copy['similarity_score'] = similarity
                doc_similarities.append(doc_copy)
            
            # 排序並返回前top_k個
            doc_similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
            return doc_similarities[:top_k]
        
        except Exception as e:
            logger.error(f"語義檢索失敗: {e}")
            return self._keyword_retrieve(query, top_k)
    
    def _keyword_retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """關鍵詞檢索（後備方案）"""
        results = []
        query_lower = query.lower()
        
        for doc in self.knowledge_base:
            content = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            
            # 計算關鍵詞匹配分數
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in content:
                    score += content.count(word) / len(query_words)
            
            if score > 0:
                doc_copy = doc.copy()
                doc_copy['similarity_score'] = min(score, 1.0)
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
                f"標題: {doc['title']}\n內容: {doc['content']}"
                for doc in context_docs
            ])
            
            # 構建提示詞
            messages = [
                {
                    "role": "system",
                    "content": "您是一位專業的財經顧問，專門回答股票投資相關問題。請基於提供的上下文資訊回答用戶問題，用繁體中文回答，並保持專業和準確。"
                },
                {
                    "role": "user",
                    "content": f"上下文資訊:\n{context}\n\n用戶問題: {query}\n\n請基於上述資訊回答問題："
                }
            ]
            
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.config.get('openai_model', 'gpt-3.5-turbo'),
                'messages': messages,
                'max_tokens': self.config.get('max_tokens', 500),
                'temperature': self.config.get('temperature', 0.7)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content'].strip()
                    else:
                        logger.error(f"OpenAI API 錯誤: {response.status}")
                        return self._template_generate(query, context_docs)
        
        except Exception as e:
            logger.error(f"OpenAI 生成回答失敗: {e}")
            return self._template_generate(query, context_docs)
    
    def _template_generate(self, query: str, context_docs: List[Dict]) -> str:
        """模板生成回答（後備方案）"""
        if not context_docs:
            return "抱歉，我沒有找到相關的資訊來回答您的問題。"
        
        best_doc = context_docs[0]
        
        # 簡單的模板回答
        response = f"根據我的了解，{best_doc['content']}"
        
        if len(context_docs) > 1:
            response += f"\n\n另外，關於{context_docs[1]['title']}也值得您了解。"
        
        return response
    
    async def query(self, question: str) -> Dict[str, Any]:
        """主查詢介面"""
        start_time = datetime.now()
        
        try:
            # 檢索相關文檔
            context_docs = await self.retrieve_documents(question, 
                                                       top_k=self.config.get('top_k_retrieve', 3))
            
            # 生成回答
            answer = await self.generate_response(question, context_docs)
            
            # 計算信心度
            confidence = self._calculate_confidence(context_docs)
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": [
                    {
                        "title": doc["title"],
                        "similarity": doc.get("similarity_score", 0),
                        "category": doc.get("category", "")
                    }
                    for doc in context_docs
                ],
                "response_time": response_time,
                "method": "openai_semantic" if self.has_openai else "keyword_template"
            }
            
        except Exception as e:
            logger.error(f"查詢處理失敗: {e}")
            return {
                "answer": f"處理您的問題時發生錯誤: {str(e)}",
                "confidence": 0.0,
                "sources": [],
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    def _calculate_confidence(self, context_docs: List[Dict]) -> float:
        """計算回答信心度"""
        if not context_docs:
            return 0.0
        
        max_score = max(doc.get('similarity_score', 0) for doc in context_docs)
        return min(max_score, 1.0)
    
    def add_knowledge(self, documents: List[Dict[str, Any]]):
        """添加知識到知識庫"""
        for doc in documents:
            if 'id' not in doc:
                doc['id'] = f"doc_{len(self.knowledge_base)}"
            if 'timestamp' not in doc:
                doc['timestamp'] = datetime.now().isoformat()
            
            self.knowledge_base.append(doc)
        
        logger.info(f"添加了 {len(documents)} 條新知識")
        
        # 保存到文件
        try:
            Path("data").mkdir(exist_ok=True)
            with open("data/knowledge_base.json", 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存知識庫失敗: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取系統統計"""
        return {
            "knowledge_base_size": len(self.knowledge_base),
            "has_openai": self.has_openai,
            "embedding_cache_size": len(self.embeddings_cache),
            "system_type": "lightweight_rag"
        } 