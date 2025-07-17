#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
進階RAG系統安裝和配置腳本
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any

def check_python_version():
    """檢查Python版本"""
    print(f"🔍 當前Python版本: {sys.version}")
    
    if sys.version_info < (3, 7, 0):
        print("❌ Python 3.7+ 是必需的")
        print("請升級您的Python版本")
        return False
    elif sys.version_info < (3, 8, 0):
        print("⚠️ 建議使用Python 3.8+以獲得最佳性能")
        print("您的版本可以運行，但某些功能可能受限")
    else:
        print("✅ Python版本符合要求")
    
    return True

def install_dependencies():
    """安裝依賴包"""
    print("📦 安裝進階RAG系統依賴...")
    
    # 基礎依賴
    basic_packages = [
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "pandas>=1.5.0"
    ]
    
    # 可選的高級依賴
    advanced_packages = [
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "openai>=1.0.0"
    ]
    
    try:
        # 安裝基礎依賴
        for package in basic_packages:
            print(f"安裝 {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
        
        print("✅ 基礎依賴安裝完成")
        
        # 嘗試安裝高級依賴
        failed_packages = []
        for package in advanced_packages:
            try:
                print(f"安裝 {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True, timeout=300)
                print(f"✅ {package} 安裝成功")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"⚠️ {package} 安裝失敗: {e}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\n⚠️ 以下套件安裝失敗，系統將使用簡化版本：")
            for pkg in failed_packages:
                print(f"  - {pkg}")
            print("這不會影響基本功能，但可能會降低性能。")
        
        return True
        
    except Exception as e:
        print(f"❌ 依賴安裝失敗: {e}")
        return False

def create_directories():
    """創建必要的目錄結構"""
    print("📁 創建目錄結構...")
    
    directories = [
        "config",
        "data",
        "logs",
        "cache/knowledge",
        "cache/vectors"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 創建目錄: {directory}")
    
    return True

def setup_configuration():
    """設置配置文件"""
    print("⚙️ 設置配置文件...")
    
    config_path = Path("config/rag_config.json")
    
    if config_path.exists():
        print("配置文件已存在，是否要重新設置？(y/n): ", end="")
        if input().lower() not in ['y', 'yes', '是']:
            print("跳過配置設置")
            return True
    
    # 互動式配置
    print("\n請設置RAG系統配置：")
    
    # OpenAI API Key
    openai_key = input("請輸入OpenAI API Key（可選，直接回車跳過）: ").strip()
    
    # 嵌入模型選擇
    print("\n選擇嵌入模型：")
    print("1. paraphrase-multilingual-MiniLM-L12-v2 (推薦，支援中文)")
    print("2. all-MiniLM-L6-v2 (較快，主要英文)")
    print("3. 使用OpenAI embeddings (需要API key)")
    
    model_choice = input("請選擇 (1-3，默認1): ").strip()
    
    embedding_models = {
        "1": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "2": "sentence-transformers/all-MiniLM-L6-v2", 
        "3": "openai"
    }
    
    embedding_model = embedding_models.get(model_choice, embedding_models["1"])
    
    # 創建配置
    config = {
        "embedding_model": embedding_model,
        "vector_db_type": "faiss",
        "openai_model": "gpt-3.5-turbo",
        "max_tokens": 500,
        "temperature": 0.7,
        "top_k_retrieve": 3,
        "confidence_threshold": 0.3,
        "openai_api_key": "YOUR_OPENAI_API_KEY_HERE",
        "fallback_to_simple": True,
        "auto_update_knowledge": False,
        "knowledge_sources": {
            "yahoo_finance": True,
            "economic_daily": True,
            "cnyes": True
        },
        "logging": {
            "level": "INFO",
            "file": "logs/rag_system.log"
        }
    }
    
    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已保存到: {config_path}")
    return True

def initialize_knowledge_base():
    """初始化知識庫"""
    print("📚 初始化知識庫...")
    
    knowledge_file = Path("data/knowledge_base.json")
    
    if knowledge_file.exists():
        print("知識庫文件已存在")
        return True
    
    # 創建初始知識庫
    initial_knowledge = [
        {
            "id": "finance_basic_001",
            "title": "股票投資入門",
            "content": "股票投資是購買公司股份，成為公司股東的投資方式。投資者透過股票價格上漲獲得資本利得，也可能獲得公司分發的股息。投資前應了解公司基本面、財務狀況和市場趨勢。",
            "category": "投資基礎",
            "source": "財經教學",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "id": "finance_basic_002",
            "title": "技術分析基礎",
            "content": "技術分析是透過股價圖表和交易量等市場數據來預測股價走勢的方法。常用工具包括移動平均線、相對強弱指數(RSI)、布林通道等。技術分析者認為股價已反映所有市場資訊。",
            "category": "技術分析",
            "source": "投資指南",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "id": "finance_basic_003",
            "title": "基本面分析",
            "content": "基本面分析評估公司的內在價值，包括財務報表分析、產業分析、經濟環境分析等。重要指標有本益比(PE)、股價淨值比(PB)、股東權益報酬率(ROE)等。",
            "category": "基本面分析",
            "source": "投資理論",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "id": "risk_management_001", 
            "title": "投資風險管理",
            "content": "風險管理是投資的核心要素，包括資產配置、分散投資、設定停損點、控制部位大小等策略。好的風險管理能幫助投資者在市場波動中保護資本並獲得穩定回報。",
            "category": "風險管理",
            "source": "投資策略",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "id": "taiwan_stock_001",
            "title": "台股市場特色",
            "content": "台灣股票市場以電子科技股為主要特色，台積電等半導體公司在全球具有重要地位。投資台股需關注國際科技趨勢、兩岸關係、匯率變化等因素。",
            "category": "台股市場",
            "source": "市場分析",
            "timestamp": "2024-01-01T00:00:00"
        }
    ]
    
    with open(knowledge_file, 'w', encoding='utf-8') as f:
        json.dump(initial_knowledge, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 知識庫已初始化: {knowledge_file}")
    return True

async def test_system():
    """測試系統功能"""
    print("🧪 測試系統功能...")
    
    try:
        # 測試導入
        from rag.core.advanced_rag import AdvancedRAGSystem, RAGConfig
        from rag.core.enhanced_chatbot import EnhancedChatBot
        
        print("✅ 模組導入成功")
        
        # 測試配置載入
        config = RAGConfig.load_config()
        print("✅ 配置載入成功")
        
        # 測試RAG系統初始化
        rag_system = AdvancedRAGSystem(config)
        print("✅ RAG系統初始化成功")
        
        # 測試增強chatbot
        chatbot = EnhancedChatBot()
        print("✅ 增強版chatbot初始化成功")
        
        # 測試查詢
        test_query = "什麼是股票投資？"
        result = await chatbot.process_message(test_query)
        print(f"✅ 測試查詢成功: {result.get('answer', '')[:50]}...")
        
        # 顯示系統狀態
        status = chatbot.get_system_status()
        print("\n📊 系統狀態:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 系統測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 進階RAG系統安裝程序")
    print("=" * 50)
    
    steps = [
        ("檢查Python版本", check_python_version),
        ("安裝依賴包", install_dependencies),
        ("創建目錄結構", create_directories), 
        ("設置配置", setup_configuration),
        ("初始化知識庫", initialize_knowledge_base)
    ]
    
    # 執行安裝步驟
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if not step_func():
                print(f"❌ {step_name}失敗")
                return False
        except Exception as e:
            print(f"❌ {step_name}失敗: {e}")
            return False
    
    # 測試系統
    print(f"\n🔄 測試系統...")
    try:
        if asyncio.run(test_system()):
            print("\n🎉 進階RAG系統安裝完成！")
            print("\n下一步:")
            print("1. 如果有OpenAI API key，請在 config/rag_config.json 中設置")
            print("2. 運行 python app.py 啟動應用")
            print("3. 訪問 http://localhost:5000/chatbot 測試chatbot")
            return True
        else:
            print("\n⚠️ 系統測試失敗，但基本安裝完成")
            print("請檢查錯誤信息並手動測試")
            return False
    except Exception as e:
        print(f"\n❌ 系統測試失敗: {e}")
        print("但基本安裝已完成，您可以手動測試系統")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 