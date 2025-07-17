#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增強版股票聊天機器人 - 整合RAG系統
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.twse import get_stock_basic_info, get_market_summary, get_stock_name
# 優先使用簡化版RAG系統
try:
    from .simple_rag import get_simple_rag_system as get_rag_system
    USE_SIMPLE_RAG = True
except ImportError:
    try:
        from .rag_system import get_rag_system
        USE_SIMPLE_RAG = False
    except ImportError:
        get_rag_system = None
        USE_SIMPLE_RAG = False
import logging

logger = logging.getLogger(__name__)

class StockChatbot:
    """增強版股票聊天機器人 - 整合RAG系統"""
    
    def __init__(self):
        # 初始化RAG系統
        try:
            if get_rag_system is not None:
                self.rag_system = get_rag_system()
                self.use_rag = True
                logger.info(f"RAG系統初始化成功 ({'簡化版' if USE_SIMPLE_RAG else '完整版'})")
            else:
                self.rag_system = None
                self.use_rag = False
                logger.warning("RAG系統不可用，使用傳統模式")
        except Exception as e:
            logger.warning(f"RAG系統初始化失敗，使用傳統模式: {e}")
            self.rag_system = None
            self.use_rag = False
        
        # 對話歷史記錄
        self.conversation_history = []
        
        # 股票代碼映射表
        self.stock_mapping = {
            '台積電': '2330',
            '鴻海': '2317',
            '聯發科': '2454',
            '台塑': '1301',
            '中華電': '2412',
            '富邦金': '2881',
            '國泰金': '2882',
            '台達電': '2308',
            '廣達': '2382',
            '元大台灣50': '0050',
            '元大高股息': '0056',
            '國泰永續高股息': '00878',
            '群益台灣精選高息': '00919',
            '富邦台50': '006208',
        }
        
        # 問候語回應
        self.greetings = [
            "您好！我是您的智能股票助手，現在擁有更豐富的知識庫，可以為您提供更全面的投資資訊和建議。",
            "歡迎使用升級版股票查詢服務！我不僅能查詢即時股價，還能回答投資相關問題。",
            "Hi！我是增強版股票助手，除了基本股票資訊外，還能為您解答投資策略、技術分析等問題。"
        ]
        
        # 查詢類型的關鍵字
        self.query_keywords = {
            'price': ['收盤價', '股價', '價格', '多少錢', '多少', '現價'],
            'change': ['漲跌', '漲幅', '跌幅', '變化'],
            'volume': ['成交量', '交易量', '成交額'],
            'basic': ['資訊', '資料', '基本資料', '詳細'],
            'market': ['大盤', '加權指數', '台股', '市場'],
            'knowledge': ['什麼是', '如何', '怎麼', '為什麼', '解釋', '說明', '投資', '策略', '分析']
        }
    
    def process_message(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """處理用戶訊息 - 增強版"""
        try:
            message = message.strip()
            
            # 記錄對話歷史
            self._add_to_history(message, 'user', user_id)
            
            # 問候語檢測
            if self.is_greeting(message):
                response = self.get_greeting_response()
                self._add_to_history(response, 'bot', user_id)
                return self._format_response(response, 'greeting')
            
            # 大盤查詢
            if self.is_market_query(message):
                response = self.get_market_response()
                self._add_to_history(response, 'bot', user_id)
                return self._format_response(response, 'market')
            
            # 股票查詢
            stock_code, query_type = self.parse_stock_query(message)
            if stock_code:
                response = self.get_stock_response(stock_code, query_type, message)
                self._add_to_history(response, 'bot', user_id)
                return self._format_response(response, 'stock', {'stock_code': stock_code, 'query_type': query_type})
            
            # 知識查詢（使用RAG系統）
            if self.use_rag and self.is_knowledge_query(message):
                response = self.get_knowledge_response(message)
                self._add_to_history(response['answer'], 'bot', user_id)
                return self._format_response(response['answer'], 'knowledge', {
                    'sources': response.get('sources', []),
                    'confidence': response.get('confidence', 0.0)
                })
            
            # 無法識別的問題
            response = self.get_help_response()
            self._add_to_history(response, 'bot', user_id)
            return self._format_response(response, 'help')
            
        except Exception as e:
            error_msg = f"抱歉，處理您的問題時發生錯誤：{str(e)}"
            self._add_to_history(error_msg, 'bot', user_id)
            return self._format_response(error_msg, 'error')
    
    def is_greeting(self, message):
        """檢測是否為問候語"""
        greetings = ['你好', '您好', 'hi', 'hello', '哈囉', '嗨', '早安', '午安', '晚安']
        return any(greeting in message.lower() for greeting in greetings)
    
    def is_market_query(self, message):
        """檢測是否為大盤查詢"""
        market_keywords = ['大盤', '加權指數', '台股指數', '市場', '整體']
        return any(keyword in message for keyword in market_keywords)
    
    def parse_stock_query(self, message):
        """解析股票查詢"""
        # 檢查是否包含股票代碼（數字）
        stock_code = None
        query_type = 'basic'
        
        # 先檢查股票名稱
        for stock_name, code in self.stock_mapping.items():
            if stock_name in message:
                stock_code = code
                break
        
        # 如果沒找到股票名稱，檢查數字代碼
        if not stock_code:
            code_match = re.search(r'\b(\d{4,6})\b', message)
            if code_match:
                stock_code = code_match.group(1)
        
        # 確定查詢類型
        if stock_code:
            for qtype, keywords in self.query_keywords.items():
                if any(keyword in message for keyword in keywords):
                    query_type = qtype
                    break
        
        return stock_code, query_type
    
    def get_greeting_response(self):
        """獲取問候回應"""
        import random
        return random.choice(self.greetings)
    
    def get_market_response(self):
        """獲取大盤資訊回應"""
        try:
            market_info = get_market_summary()
            
            if market_info and not market_info.get('錯誤'):
                response = "📊 大盤資訊：\n"
                response += f"• 加權指數：{market_info.get('指數', 'N/A')}\n"
                response += f"• 漲跌：{market_info.get('漲跌點數', 'N/A')}\n"
                response += f"• 漲跌幅：{market_info.get('漲跌幅', 'N/A')}\n"
                response += f"• 成交量：{market_info.get('成交量', 'N/A')}\n"
                response += f"• 更新時間：{market_info.get('更新時間', 'N/A')}"
                return response
            else:
                return "抱歉，目前無法獲取大盤資訊，請稍後再試。"
                
        except Exception as e:
            return f"獲取大盤資訊時發生錯誤：{str(e)}"
    
    def get_stock_response(self, stock_code, query_type, original_message):
        """獲取股票資訊回應"""
        try:
            stock_info = get_stock_basic_info(stock_code)
            
            if not stock_info or stock_info.get('錯誤'):
                return f"抱歉，無法找到股票代碼 {stock_code} 的資訊。請確認代碼是否正確。"
            
            stock_name = stock_info.get('股票名稱', stock_code)
            
            # 根據查詢類型回應
            if query_type == 'price':
                price = stock_info.get('收盤價', 'N/A')
                change = stock_info.get('漲跌價差', 'N/A')
                change_percent = stock_info.get('漲跌幅', 'N/A')
                
                response = f"📈 {stock_name} ({stock_code}) 價格資訊：\n"
                response += f"• 收盤價：{price}\n"
                response += f"• 漲跌：{change}\n"
                response += f"• 漲跌幅：{change_percent}"
                
            elif query_type == 'change':
                change = stock_info.get('漲跌價差', 'N/A')
                change_percent = stock_info.get('漲跌幅', 'N/A')
                
                response = f"📊 {stock_name} ({stock_code}) 漲跌資訊：\n"
                response += f"• 漲跌：{change}\n"
                response += f"• 漲跌幅：{change_percent}"
                
            elif query_type == 'volume':
                volume = stock_info.get('成交量', stock_info.get('成交股數', 'N/A'))
                amount = stock_info.get('成交金額', 'N/A')
                
                response = f"💰 {stock_name} ({stock_code}) 成交資訊：\n"
                response += f"• 成交量：{volume}\n"
                response += f"• 成交金額：{amount}"
                
            else:  # basic info
                response = f"📋 {stock_name} ({stock_code}) 基本資訊：\n"
                response += f"• 收盤價：{stock_info.get('收盤價', 'N/A')}\n"
                response += f"• 漲跌：{stock_info.get('漲跌價差', 'N/A')}\n"
                response += f"• 漲跌幅：{stock_info.get('漲跌幅', 'N/A')}\n"
                response += f"• 開盤價：{stock_info.get('開盤價', 'N/A')}\n"
                response += f"• 最高價：{stock_info.get('最高價', 'N/A')}\n"
                response += f"• 最低價：{stock_info.get('最低價', 'N/A')}\n"
                response += f"• 成交量：{stock_info.get('成交量', 'N/A')}"
            
            return response
            
        except Exception as e:
            return f"查詢股票資訊時發生錯誤：{str(e)}"
    
    def is_knowledge_query(self, message: str) -> bool:
        """檢測是否為知識查詢"""
        knowledge_keywords = self.query_keywords['knowledge']
        return any(keyword in message for keyword in knowledge_keywords)
    
    def get_knowledge_response(self, message: str) -> Dict[str, Any]:
        """使用RAG系統獲取知識回應"""
        try:
            if not self.use_rag:
                return {
                    'answer': "抱歉，知識查詢功能目前不可用。",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # 獲取對話上下文
            context = self._get_conversation_context()
            
            # 使用RAG系統查詢
            rag_response = self.rag_system.query(message, context)
            
            return rag_response
            
        except Exception as e:
            logger.error(f"知識查詢失敗: {e}")
            return {
                'answer': f"抱歉，查詢知識時發生錯誤：{str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def _add_to_history(self, message: str, sender: str, user_id: str = None):
        """添加對話到歷史記錄"""
        self.conversation_history.append({
            'message': message,
            'sender': sender,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        })
        
        # 保持歷史記錄在合理範圍內
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def _get_conversation_context(self) -> Dict[str, Any]:
        """獲取對話上下文"""
        return {
            'recent_messages': self.conversation_history[-5:] if self.conversation_history else [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_response(self, answer: str, response_type: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """格式化回應"""
        return {
            'answer': answer,
            'type': response_type,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'enhanced': self.use_rag
        }
    
    def get_help_response(self):
        """獲取幫助回應"""
        base_help = """🤖 我是您的智能股票助手，可以幫您查詢以下資訊：

📊 **大盤查詢**
• "大盤怎麼樣？"
• "加權指數多少？"

📈 **股票查詢**
• "台積電今天收盤多少？"
• "2330股價多少？"
• "鴻海漲跌幅如何？"
• "0050成交量多少？"

💡 **支援的股票**
台積電、鴻海、聯發科、台塑、中華電、富邦金、國泰金、台達電、廣達、元大台灣50、元大高股息等

您也可以直接輸入4-6位數的股票代碼進行查詢。"""
        
        if self.use_rag:
            enhanced_help = """

🧠 **知識查詢** (NEW!)
• "什麼是本益比？"
• "如何分析股票？"
• "價值投資策略是什麼？"
• "技術分析怎麼看？"
• "ROE是什麼意思？"

💎 **投資建議**
• "新手該如何開始投資？"
• "ETF和個股有什麼差別？"
• "如何分散投資風險？"

我現在擁有豐富的財經知識庫，可以回答更多投資相關問題！"""
            return base_help + enhanced_help
        
        return base_help

# 全域聊天機器人實例
chatbot = StockChatbot()

def process_chat_message(message: str, user_id: str = None) -> str:
    """處理聊天訊息的主要函數"""
    try:
        response = chatbot.process_message(message, user_id)
        
        # 如果是新格式的回應，提取answer部分
        if isinstance(response, dict) and 'answer' in response:
            return response['answer']
        
        # 向後兼容舊格式
        return str(response)
        
    except Exception as e:
        logger.error(f"處理聊天訊息失敗: {e}")
        return f"抱歉，處理您的問題時發生錯誤：{str(e)}"

def process_chat_message_enhanced(message: str, user_id: str = None) -> Dict[str, Any]:
    """處理聊天訊息的增強函數（返回完整回應）"""
    return chatbot.process_message(message, user_id) 