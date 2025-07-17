#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增強版Chatbot - 整合進階RAG系統和語言模型
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# 嘗試導入進階RAG系統
try:
    from .advanced_rag import AdvancedRAGSystem, RAGConfig
    HAS_ADVANCED_RAG = True
except ImportError:
    HAS_ADVANCED_RAG = False

# 後備方案：使用簡化RAG系統
try:
    from .simple_rag import SimpleRAGSystem
    HAS_SIMPLE_RAG = True
except ImportError:
    HAS_SIMPLE_RAG = False

# 原始chatbot功能
try:
    from .chatbot import ChatBot as OriginalChatBot
    HAS_ORIGINAL_CHATBOT = True
except ImportError:
    HAS_ORIGINAL_CHATBOT = False

logger = logging.getLogger(__name__)

class EnhancedChatBot:
    """增強版聊天機器人 - 整合多種RAG系統"""
    
    def __init__(self, config_file: str = "config/rag_config.json"):
        """
        初始化增強版聊天機器人
        
        Args:
            config_file: 配置文件路徑
        """
        self.config = self._load_config(config_file)
        self.conversation_history = []
        self.rag_system = None
        self.original_chatbot = None
        
        # 初始化RAG系統
        self._initialize_rag_system()
        
        # 初始化原始chatbot作為後備
        if HAS_ORIGINAL_CHATBOT:
            try:
                self.original_chatbot = OriginalChatBot()
                logger.info("原始chatbot初始化完成")
            except Exception as e:
                logger.warning(f"原始chatbot初始化失敗: {e}")
        
        logger.info("增強版聊天機器人初始化完成")
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """載入配置"""
        if HAS_ADVANCED_RAG:
            return RAGConfig.load_config(config_file)
        else:
            return {
                "fallback_to_simple": True,
                "confidence_threshold": 0.3
            }
    
    def _initialize_rag_system(self):
        """初始化RAG系統"""
        try:
            # 嘗試使用進階RAG系統
            if HAS_ADVANCED_RAG:
                self.rag_system = AdvancedRAGSystem(self.config)
                if self.rag_system.initialized:
                    logger.info("進階RAG系統初始化成功")
                    return
            
            # 後備：使用簡化RAG系統
            if HAS_SIMPLE_RAG and self.config.get('fallback_to_simple', True):
                self.rag_system = SimpleRAGSystem()
                logger.info("使用簡化RAG系統作為後備")
                return
            
            logger.warning("無法初始化任何RAG系統")
            
        except Exception as e:
            logger.error(f"RAG系統初始化失敗: {e}")
            self.rag_system = None
    
    async def process_message(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """
        處理用戶消息
        
        Args:
            message: 用戶消息
            user_id: 用戶ID
            
        Returns:
            包含回答和元數據的字典
        """
        start_time = datetime.now()
        
        # 記錄對話歷史
        self.conversation_history.append({
            "user_id": user_id,
            "message": message,
            "timestamp": start_time.isoformat(),
            "type": "user"
        })
        
        try:
            # 判斷消息類型並路由到相應處理器
            response = await self._route_message(message, user_id)
            
            # 記錄回答歷史
            self.conversation_history.append({
                "user_id": user_id,
                "message": response.get("answer", ""),
                "timestamp": datetime.now().isoformat(),
                "type": "assistant",
                "metadata": response
            })
            
            return response
            
        except Exception as e:
            logger.error(f"處理消息失敗: {e}")
            error_response = {
                "answer": f"抱歉，處理您的消息時發生錯誤：{str(e)}",
                "confidence": 0.0,
                "message_type": "error",
                "response_time": (datetime.now() - start_time).total_seconds()
            }
            
            # 記錄錯誤
            self.conversation_history.append({
                "user_id": user_id,
                "message": error_response["answer"],
                "timestamp": datetime.now().isoformat(),
                "type": "error",
                "metadata": error_response
            })
            
            return error_response
    
    async def _route_message(self, message: str, user_id: str) -> Dict[str, Any]:
        """路由消息到相應處理器"""
        message_lower = message.lower().strip()
        
        # 1. 問候處理
        if any(greeting in message_lower for greeting in ['你好', 'hello', 'hi', '哈囉', '嗨']):
            return await self._handle_greeting(message, user_id)
        
        # 2. 股價查詢（包含數字的可能是股票代碼）
        if any(keyword in message_lower for keyword in ['股價', '價格', '多少錢', '現價']) or message.isdigit():
            return await self._handle_stock_query(message, user_id)
        
        # 3. 大盤查詢
        if any(keyword in message_lower for keyword in ['大盤', '指數', '台股', '加權']):
            return await self._handle_market_query(message, user_id)
        
        # 4. 知識查詢（使用RAG系統）
        return await self._handle_knowledge_query(message, user_id)
    
    async def _handle_greeting(self, message: str, user_id: str) -> Dict[str, Any]:
        """處理問候"""
        return {
            "answer": "您好！我是您的財經助手，可以幫您查詢股價、解答投資問題。請問有什麼可以協助您的嗎？",
            "confidence": 1.0,
            "message_type": "greeting",
            "response_time": 0.1,
            "sources": []
        }
    
    async def _handle_stock_query(self, message: str, user_id: str) -> Dict[str, Any]:
        """處理股價查詢"""
        if self.original_chatbot:
            try:
                # 使用原始chatbot的股價查詢功能
                if hasattr(self.original_chatbot, 'query_stock_async'):
                    result = await self.original_chatbot.query_stock_async(message)
                else:
                    # 同步版本
                    result = self.original_chatbot.query_stock(message)
                
                return {
                    "answer": result,
                    "confidence": 0.9,
                    "message_type": "stock_query",
                    "response_time": 0.5,
                    "sources": [{"title": "即時股價", "type": "real_time_data"}]
                }
            except Exception as e:
                logger.error(f"股價查詢失敗: {e}")
        
        return {
            "answer": "抱歉，目前無法查詢股價資訊。請稍後再試。",
            "confidence": 0.0,
            "message_type": "stock_query_error",
            "response_time": 0.1
        }
    
    async def _handle_market_query(self, message: str, user_id: str) -> Dict[str, Any]:
        """處理大盤查詢"""
        if self.original_chatbot:
            try:
                # 使用原始chatbot的大盤查詢功能
                if hasattr(self.original_chatbot, 'query_market_async'):
                    result = await self.original_chatbot.query_market_async(message)
                else:
                    result = self.original_chatbot.query_market(message)
                
                return {
                    "answer": result,
                    "confidence": 0.9,
                    "message_type": "market_query",
                    "response_time": 0.5,
                    "sources": [{"title": "大盤指數", "type": "real_time_data"}]
                }
            except Exception as e:
                logger.error(f"大盤查詢失敗: {e}")
        
        return {
            "answer": "抱歉，目前無法查詢大盤資訊。請稍後再試。",
            "confidence": 0.0,
            "message_type": "market_query_error",
            "response_time": 0.1
        }
    
    async def _handle_knowledge_query(self, message: str, user_id: str) -> Dict[str, Any]:
        """處理知識查詢"""
        if not self.rag_system:
            return {
                "answer": "抱歉，知識查詢系統目前不可用。",
                "confidence": 0.0,
                "message_type": "knowledge_query_error",
                "response_time": 0.1
            }
        
        try:
            # 使用RAG系統查詢
            if hasattr(self.rag_system, 'query') and asyncio.iscoroutinefunction(self.rag_system.query):
                # 進階RAG系統（異步）
                result = await self.rag_system.query(message)
            else:
                # 簡化RAG系統（同步）
                if hasattr(self.rag_system, 'query'):
                    result = self.rag_system.query(message)
                else:
                    # 簡化版本的搜索
                    docs = self.rag_system.search_knowledge(message)
                    result = {
                        "answer": docs[0]["content"] if docs else "沒有找到相關資訊",
                        "confidence": docs[0].get("confidence", 0.0) if docs else 0.0,
                        "sources": docs[:3] if docs else []
                    }
            
            # 確保結果格式一致
            if isinstance(result, str):
                result = {"answer": result, "confidence": 0.5}
            
            result["message_type"] = "knowledge_query"
            return result
            
        except Exception as e:
            logger.error(f"知識查詢失敗: {e}")
            return {
                "answer": f"知識查詢時發生錯誤：{str(e)}",
                "confidence": 0.0,
                "message_type": "knowledge_query_error",
                "response_time": 0.1
            }
    
    def get_conversation_history(self, user_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """獲取對話歷史"""
        history = self.conversation_history
        
        if user_id:
            history = [msg for msg in history if msg.get("user_id") == user_id]
        
        return history[-limit:] if limit else history
    
    def clear_conversation_history(self, user_id: str = None):
        """清除對話歷史"""
        if user_id:
            self.conversation_history = [
                msg for msg in self.conversation_history 
                if msg.get("user_id") != user_id
            ]
        else:
            self.conversation_history = []
    
    async def add_knowledge(self, documents: List[Dict[str, Any]]) -> bool:
        """添加知識到系統"""
        if not self.rag_system:
            return False
        
        try:
            if hasattr(self.rag_system, 'add_knowledge'):
                if asyncio.iscoroutinefunction(self.rag_system.add_knowledge):
                    await self.rag_system.add_knowledge(documents)
                else:
                    self.rag_system.add_knowledge(documents)
                return True
        except Exception as e:
            logger.error(f"添加知識失敗: {e}")
        
        return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """獲取系統狀態"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "has_advanced_rag": HAS_ADVANCED_RAG,
            "has_simple_rag": HAS_SIMPLE_RAG,
            "has_original_chatbot": HAS_ORIGINAL_CHATBOT and self.original_chatbot is not None,
            "rag_system_initialized": self.rag_system is not None,
            "conversation_count": len(self.conversation_history)
        }
        
        # 獲取RAG系統統計
        if self.rag_system and hasattr(self.rag_system, 'get_statistics'):
            status["rag_statistics"] = self.rag_system.get_statistics()
        
        return status

# 向後兼容性：提供同步介面
class ChatBot:
    """向後兼容的ChatBot類"""
    
    def __init__(self):
        self.enhanced_bot = EnhancedChatBot()
    
    def query(self, message: str) -> str:
        """同步查詢介面"""
        try:
            # 在同步環境中運行異步函數
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已經在事件循環中，使用concurrent.futures
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.enhanced_bot.process_message(message))
                    result = future.result()
            else:
                result = asyncio.run(self.enhanced_bot.process_message(message))
            
            return result.get("answer", "系統錯誤")
        except Exception as e:
            logger.error(f"同步查詢失敗: {e}")
            return f"查詢失敗：{str(e)}"
    
    async def query_async(self, message: str) -> Dict[str, Any]:
        """異步查詢介面"""
        return await self.enhanced_bot.process_message(message)
    
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """搜索知識庫"""
        if self.enhanced_bot.rag_system and hasattr(self.enhanced_bot.rag_system, 'search_knowledge'):
            return self.enhanced_bot.rag_system.search_knowledge(query)
        return [] 