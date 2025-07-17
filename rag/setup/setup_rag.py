#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG系統初始化腳本
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_dependencies():
    """安裝必要的依賴"""
    try:
        logger.info("開始安裝RAG系統依賴...")
        
        # 檢查是否存在requirements_rag.txt
        if not Path('requirements_rag.txt').exists():
            logger.error("requirements_rag.txt 文件不存在")
            return False
        
        # 安裝依賴
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_rag.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("依賴安裝成功")
            return True
        else:
            logger.error(f"依賴安裝失敗: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"安裝依賴時發生錯誤: {e}")
        return False

def create_directories():
    """創建必要的目錄"""
    try:
        directories = [
            'data/knowledge',
            'cache/knowledge',
            'cache/vector_store',
            'cache/embeddings'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"創建目錄: {directory}")
        
        return True
        
    except Exception as e:
        logger.error(f"創建目錄時發生錯誤: {e}")
        return False

def initialize_knowledge_base():
    """初始化知識庫"""
    try:
        logger.info("開始初始化知識庫...")
        
        # 導入並運行知識庫初始化
        from utils.knowledge_initializer import initialize_knowledge_base
        
        success = initialize_knowledge_base()
        
        if success:
            logger.info("知識庫初始化成功")
            return True
        else:
            logger.error("知識庫初始化失敗")
            return False
            
    except Exception as e:
        logger.error(f"初始化知識庫時發生錯誤: {e}")
        return False

def test_rag_system():
    """測試RAG系統"""
    try:
        logger.info("開始測試RAG系統...")
        
        from rag.core.rag_system import get_rag_system
        
        # 初始化RAG系統
        rag_system = get_rag_system()
        
        # 測試查詢
        test_query = "什麼是股票？"
        response = rag_system.query(test_query)
        
        logger.info(f"測試查詢: {test_query}")
        logger.info(f"回應: {response['answer'][:100]}...")
        
        if response['answer']:
            logger.info("RAG系統測試成功")
            return True
        else:
            logger.error("RAG系統測試失敗")
            return False
            
    except Exception as e:
        logger.error(f"測試RAG系統時發生錯誤: {e}")
        return False

def test_chatbot():
    """測試增強版聊天機器人"""
    try:
        logger.info("開始測試增強版聊天機器人...")
        
        from utils.chatbot import process_chat_message_enhanced
        
        # 測試問題
        test_questions = [
            "你好",
            "台積電股價多少？",
            "什麼是本益比？",
            "大盤怎麼樣？"
        ]
        
        for question in test_questions:
            response = process_chat_message_enhanced(question)
            logger.info(f"問題: {question}")
            logger.info(f"回應類型: {response.get('type', 'unknown')}")
            logger.info(f"回應: {response.get('answer', 'no answer')[:100]}...")
            logger.info("-" * 50)
        
        logger.info("聊天機器人測試完成")
        return True
        
    except Exception as e:
        logger.error(f"測試聊天機器人時發生錯誤: {e}")
        return False

def main():
    """主函數"""
    logger.info("開始RAG系統初始化...")
    
    steps = [
        ("安裝依賴", install_dependencies),
        ("創建目錄", create_directories),
        ("初始化知識庫", initialize_knowledge_base),
        ("測試RAG系統", test_rag_system),
        ("測試聊天機器人", test_chatbot)
    ]
    
    for step_name, step_func in steps:
        logger.info(f"執行步驟: {step_name}")
        
        if not step_func():
            logger.error(f"步驟失敗: {step_name}")
            logger.error("RAG系統初始化失敗")
            return False
        
        logger.info(f"步驟完成: {step_name}")
    
    logger.info("🎉 RAG系統初始化完成！")
    logger.info("您的聊天機器人現在擁有以下增強功能：")
    logger.info("• 知識查詢：可以回答投資相關問題")
    logger.info("• 對話記憶：記住對話上下文")
    logger.info("• 來源追蹤：顯示回答的資料來源")
    logger.info("• 信心評分：評估回答的可信度")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 