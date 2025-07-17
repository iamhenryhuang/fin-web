#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單演示腳本 - 展示RAG系統的實際使用效果
"""

import asyncio
import sys
from pathlib import Path

def demonstrate_simple_rag():
    """演示簡化版RAG系統"""
    print("🎯 簡化版RAG系統演示")
    print("=" * 50)
    
    try:
        from rag.core.simple_rag import SimpleRAGSystem
        
        # 初始化系統
        rag = SimpleRAGSystem()
        print("✅ 系統初始化成功")
        
        # 測試查詢
        test_queries = [
            "什麼是本益比？",
            "價值投資是什麼？",
            "如何看移動平均線？",
            "RSI指標怎麼用？",
            "投資有什麼風險？"
        ]
        
        print(f"\n📋 測試查詢 ({len(test_queries)} 個問題):")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- 問題 {i}: {query} ---")
            
            result = rag.query(query)
            
            print(f"✅ 回答:")
            print(f"   {result['answer']}")
            print(f"📊 信心度: {result['confidence']:.3f}")
            
            if result.get('sources'):
                print(f"📚 來源: {result['sources'][0]['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失敗: {e}")
        return False

async def demonstrate_enhanced_chatbot():
    """演示增強版chatbot（如果可用）"""
    print(f"\n🤖 增強版Chatbot演示")
    print("=" * 50)
    
    try:
        from utils.enhanced_chatbot import ChatBot
        
        # 使用向後兼容的同步介面
        chatbot = ChatBot()
        print("✅ Chatbot初始化成功")
        
        # 測試各種類型的查詢
        test_scenarios = [
            ("問候", "你好"),
            ("知識查詢", "什麼是技術分析？"),
            ("投資建議", "新手應該怎麼開始投資？")
        ]
        
        for scenario_type, query in test_scenarios:
            print(f"\n--- {scenario_type}: {query} ---")
            try:
                result = chatbot.query(query)
                print(f"✅ 回答: {result}")
            except Exception as e:
                print(f"⚠️ 查詢失敗: {e}")
        
        return True
        
    except ImportError:
        print("⚠️ 增強版Chatbot不可用，使用基本版本")
        return demonstrate_basic_chatbot()
    except Exception as e:
        print(f"❌ 增強版Chatbot演示失敗: {e}")
        return False

def demonstrate_basic_chatbot():
    """演示基本chatbot"""
    try:
        from utils.chatbot import ChatBot
        
        chatbot = ChatBot()
        print("✅ 基本Chatbot初始化成功")
        
        test_queries = [
            "你好",
            "什麼是股票？",
            "2330"  # 台積電股票代碼
        ]
        
        for query in test_queries:
            print(f"\n查詢: {query}")
            try:
                result = chatbot.query(query)
                print(f"回答: {result[:100]}...")
            except Exception as e:
                print(f"查詢失敗: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本chatbot演示失敗: {e}")
        return False

def show_system_capabilities():
    """展示系統能力"""
    print(f"\n💡 系統能力總覽")
    print("=" * 50)
    
    capabilities = {
        "✅ 財經知識查詢": [
            "本益比、股價淨值比等財務指標",
            "技術分析工具和方法",
            "投資策略和風險管理",
            "台股市場特色"
        ],
        "✅ 智能回答生成": [
            "基於知識庫的語義搜索",
            "上下文相關的回答",
            "信心度評估",
            "來源追蹤"
        ],
        "✅ 多層次回退機制": [
            "進階RAG + OpenAI GPT",
            "本地嵌入模型",
            "關鍵詞匹配",
            "模板回答"
        ]
    }
    
    for category, items in capabilities.items():
        print(f"\n{category}")
        for item in items:
            print(f"  • {item}")

def show_integration_guide():
    """展示整合指南"""
    print(f"\n🔧 整合到您的應用")
    print("=" * 50)
    
    print("1. 基本RAG查詢:")
    print("""
from rag.core.simple_rag import SimpleRAGSystem

rag = SimpleRAGSystem()
result = rag.query("什麼是本益比？")
print(result["answer"])
""")
    
    print("2. Chatbot整合:")
    print("""
from utils.chatbot import ChatBot

chatbot = ChatBot()
response = chatbot.query("你好，我想了解股票投資")
print(response)
""")
    
    print("3. Web應用整合:")
    print("""
# 在您的Flask/Django應用中
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chatbot = ChatBot()
    response = chatbot.query(user_message)
    return {"response": response}
""")
    
    print("4. 添加新知識:")
    print("""
rag = SimpleRAGSystem()
new_docs = [
    {
        "title": "新投資概念",
        "content": "詳細說明...",
        "category": "投資策略"
    }
]
rag.add_knowledge(new_docs)
""")

def main():
    """主函數"""
    print("🚀 RAG系統完整演示")
    print("=" * 60)
    
    print("本演示將展示:")
    print("• 簡化版RAG系統的知識查詢能力")
    print("• Chatbot的對話功能")  
    print("• 系統整合方法")
    print("• 實際使用案例")
    
    # 檢查基本文件
    required_files = ["utils/simple_rag.py", "utils/chatbot.py"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"\n❌ 缺少必要文件: {missing_files}")
        return False
    
    # 運行演示
    results = []
    
    # 1. 簡化RAG演示
    results.append(demonstrate_simple_rag())
    
    # 2. Chatbot演示  
    results.append(asyncio.run(demonstrate_enhanced_chatbot()))
    
    # 總結
    passed = sum(results)
    total = len(results)
    
    print(f"\n" + "="*60)
    print(f"📊 演示結果: {passed}/{total} 成功")
    
    if passed > 0:
        print("🎉 系統基本功能正常！")
        
        # 展示系統能力
        show_system_capabilities()
        
        # 整合指南
        show_integration_guide()
        
        print(f"\n📚 進一步學習:")
        print("• 查看 RAG_整合指南.md 了解進階功能")
        print("• 運行 python setup_advanced_rag.py 安裝完整系統")
        print("• 編輯 config/rag_config.json 配置OpenAI API")
        
    else:
        print("❌ 系統存在問題，請檢查安裝")
    
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 