#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
輕量級RAG系統測試腳本
"""

import asyncio
import json
from pathlib import Path

async def test_lightweight_rag():
    """測試輕量級RAG系統"""
    print("🧪 測試輕量級RAG系統...")
    
    try:
        from rag.core.lightweight_rag import LightweightRAGSystem
        
        # 初始化系統
        rag = LightweightRAGSystem()
        print("✅ 輕量級RAG系統初始化成功")
        
        # 顯示系統狀態
        stats = rag.get_statistics()
        print(f"📊 系統狀態:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        # 測試各種查詢
        test_queries = [
            "什麼是股票投資？",
            "如何做基本面分析？", 
            "技術分析有哪些指標？",
            "投資有什麼風險？",
            "台股市場有什麼特色？"
        ]
        
        print(f"\n🔍 測試查詢...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- 測試 {i}: {query} ---")
            
            result = await rag.query(query)
            
            print(f"✅ 查詢成功")
            print(f"回答: {result['answer'][:150]}...")
            print(f"信心度: {result['confidence']:.3f}")
            print(f"檢索方法: {result['method']}")
            print(f"回應時間: {result['response_time']:.2f}秒")
            
            if result['sources']:
                print(f"來源文檔:")
                for source in result['sources']:
                    print(f"  - {source['title']} (相似度: {source['similarity']:.3f})")
        
        # 測試添加新知識
        print(f"\n📚 測試添加新知識...")
        
        new_knowledge = [
            {
                "title": "ESG投資",
                "content": "ESG投資是考慮環境(Environmental)、社會(Social)、治理(Governance)因素的投資方式。這種投資策略不僅關注財務回報，也重視企業的永續經營和社會責任。",
                "category": "投資策略"
            }
        ]
        
        rag.add_knowledge(new_knowledge)
        print("✅ 新知識添加成功")
        
        # 測試新添加的知識
        result = await rag.query("什麼是ESG投資？")
        print(f"✅ 新知識查詢測試:")
        print(f"回答: {result['answer'][:100]}...")
        print(f"信心度: {result['confidence']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 輕量級RAG測試失敗: {e}")
        return False

async def demo_usage():
    """演示使用方式"""
    print("\n" + "="*60)
    print("📖 輕量級RAG系統使用演示")
    print("="*60)
    
    try:
        from utils.lightweight_rag import LightweightRAGSystem
        
        # 創建RAG系統實例
        rag = LightweightRAGSystem()
        
        print("💡 這個系統的特點:")
        print("1. 如果有OpenAI API key，使用真實的語義搜索和GPT生成")
        print("2. 如果沒有API key，自動回退到關鍵詞匹配和模板回答")
        print("3. 不依賴複雜的機器學習庫（如sentence-transformers）")
        print("4. 輕量級，易於部署和維護")
        
        # 互動式查詢演示
        print(f"\n🤖 互動式查詢演示:")
        
        demo_queries = [
            ("基礎問題", "什麼是股票？"),
            ("專業概念", "本益比怎麼計算？"),
            ("投資策略", "新手應該怎麼投資？")
        ]
        
        for category, query in demo_queries:
            print(f"\n{category}: {query}")
            result = await rag.query(query)
            print(f"回答: {result['answer']}")
            print(f"(信心度: {result['confidence']:.2f}, 方法: {result['method']})")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失敗: {e}")
        return False

async def main():
    """主函數"""
    print("🚀 輕量級RAG系統測試和演示")
    print("=" * 60)
    
    # 檢查依賴
    print("🔍 檢查依賴...")
    try:
        import aiohttp
        print("✅ aiohttp 可用")
    except ImportError:
        print("❌ 需要安裝 aiohttp: pip install aiohttp")
        return
    
    # 檢查配置
    config_file = Path("config/rag_config.json")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get('openai_api_key', '')
        if api_key and api_key.startswith('sk-'):
            print("✅ OpenAI API key 已配置")
            print("   系統將使用語義搜索和GPT生成回答")
        else:
            print("⚠️ 未配置OpenAI API key")
            print("   系統將使用關鍵詞匹配和模板回答")
    else:
        print("⚠️ 配置文件不存在，使用預設設定")
    
    # 運行測試
    success = await test_lightweight_rag()
    
    if success:
        await demo_usage()
        
        print(f"\n" + "="*60)
        print("🎉 測試完成！")
        print("="*60)
        
        print("📋 系統特色總結:")
        print("✅ 無需複雜的機器學習依賴")
        print("✅ 智能回退機制（OpenAI ↔ 關鍵詞匹配）")
        print("✅ 動態知識庫管理")
        print("✅ 快速部署和使用")
        
        print("\n🔧 如何整合到您的應用:")
        print("""
# 基本使用
from utils.lightweight_rag import LightweightRAGSystem
import asyncio

async def main():
    rag = LightweightRAGSystem()
    result = await rag.query("什麼是股票投資？")
    print(result["answer"])

asyncio.run(main())
""")
        
        print("📚 進一步使用:")
        print("- 編輯 config/rag_config.json 來配置OpenAI API")
        print("- 在 data/knowledge_base.json 中添加更多知識")
        print("- 整合到您的web應用或chatbot中")
    
    else:
        print("❌ 測試失敗，請檢查錯誤信息")

if __name__ == "__main__":
    asyncio.run(main()) 