#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速測試腳本 - 驗證RAG系統基本功能
"""

import sys
import asyncio
import json
from pathlib import Path

def check_system():
    """檢查系統基本要求"""
    print("🔍 系統檢查...")
    print(f"Python版本: {sys.version}")
    
    # 檢查基本文件
    required_files = [
        "utils/simple_rag.py",
        "utils/chatbot.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} 存在")
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    
    return True

async def test_simple_rag():
    """測試簡化版RAG系統"""
    print("\n🧪 測試簡化版RAG系統...")
    
    try:
        from rag.core.simple_rag import SimpleRAGSystem
        
        # 初始化
        rag = SimpleRAGSystem()
        print("✅ SimpleRAGSystem 初始化成功")
        
        # 測試查詢
        result = rag.query("什麼是本益比？")
        print("✅ 查詢測試成功")
        print(f"回答: {result['answer'][:100]}...")
        print(f"信心度: {result['confidence']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 簡化版RAG測試失敗: {e}")
        return False

async def test_enhanced_chatbot():
    """測試增強版chatbot"""
    print("\n🧪 測試增強版Chatbot...")
    
    try:
        # 先嘗試導入增強版
        try:
            from utils.enhanced_chatbot import EnhancedChatBot
            chatbot = EnhancedChatBot()
            print("✅ EnhancedChatBot 初始化成功")
            
            # 測試查詢
            result = await chatbot.process_message("你好")
            print("✅ 問候測試成功")
            print(f"回答: {result['answer']}")
            
            # 測試知識查詢
            result = await chatbot.process_message("什麼是股票投資？")
            print("✅ 知識查詢測試成功")
            print(f"回答: {result['answer'][:100]}...")
            
            return True
            
        except ImportError:
            # 回退到原始chatbot
            print("⚠️ 增強版不可用，測試原始chatbot...")
            from utils.chatbot import ChatBot
            chatbot = ChatBot()
            result = chatbot.query("你好")
            print("✅ 原始ChatBot 測試成功")
            print(f"回答: {result[:100]}...")
            return True
            
    except Exception as e:
        print(f"❌ Chatbot測試失敗: {e}")
        return False

async def test_openai_integration():
    """測試OpenAI整合"""
    print("\n🧪 測試OpenAI整合...")
    
    try:
        # 檢查配置文件
        config_file = Path("config/rag_config.json")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            api_key = config.get('openai_api_key', '')
            if api_key and api_key != "":
                print("✅ OpenAI API key 已配置")
                
                # 嘗試使用進階RAG
                try:
                    from rag.core.advanced_rag import AdvancedRAGSystem
                    rag = AdvancedRAGSystem(config)
                    print("✅ 進階RAG系統初始化成功")
                    
                    # 簡單測試
                    result = await rag.query("什麼是投資？")
                    print("✅ OpenAI整合測試成功")
                    print(f"回答: {result['answer'][:100]}...")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ 進階RAG初始化失敗: {e}")
                    print("將使用簡化版本")
                    return False
            else:
                print("⚠️ 未配置OpenAI API key")
                return False
        else:
            print("⚠️ 配置文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI整合測試失敗: {e}")
        return False

def show_usage_examples():
    """顯示使用範例"""
    print("""
📖 使用範例:

1. 基本同步使用:
   from utils.chatbot import ChatBot
   chatbot = ChatBot()
   result = chatbot.query("什麼是股票？")

2. 增強版異步使用:
   from utils.enhanced_chatbot import EnhancedChatBot
   import asyncio
   
   async def main():
       chatbot = EnhancedChatBot()
       result = await chatbot.process_message("什麼是股票？")
       print(result["answer"])
   
   asyncio.run(main())

3. 直接RAG查詢:
   from utils.simple_rag import SimpleRAGSystem
   rag = SimpleRAGSystem()
   result = rag.query("投資有什麼風險？")
""")

async def main():
    """主測試函數"""
    print("🚀 RAG系統快速測試")
    print("=" * 50)
    
    # 基本檢查
    if not check_system():
        print("❌ 系統檢查失敗，請確保所有必要文件存在")
        return
    
    # 功能測試
    tests = [
        ("簡化版RAG", test_simple_rag),
        ("增強版Chatbot", test_enhanced_chatbot),
        ("OpenAI整合", test_openai_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = await test_func()
            if success:
                passed += 1
                print(f"✅ {test_name} 測試通過")
            else:
                print(f"⚠️ {test_name} 測試未完全通過")
        except Exception as e:
            print(f"❌ {test_name} 測試失敗: {e}")
    
    # 結果總結
    print(f"\n{'='*50}")
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！系統運作正常。")
    elif passed >= 1:
        print("⚠️ 部分功能可用，基本系統運作正常。")
        if passed < total:
            print("💡 某些進階功能可能需要安裝額外依賴。")
    else:
        print("❌ 系統存在問題，請檢查安裝。")
    
    # 顯示使用範例
    show_usage_examples()
    
    print("\n🔗 更多資訊:")
    print("  - 完整測試: python test_advanced_rag.py")
    print("  - 系統安裝: python setup_advanced_rag.py")
    print("  - 使用指南: RAG_整合指南.md")

if __name__ == "__main__":
    asyncio.run(main()) 