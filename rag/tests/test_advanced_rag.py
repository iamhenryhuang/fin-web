#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
進階RAG系統測試腳本
"""

import asyncio
import json
import sys
from pathlib import Path

def test_imports():
    """測試模組導入"""
    print("🔍 測試模組導入...")
    
    try:
        # 測試基本導入
        from rag.core.advanced_rag import AdvancedRAGSystem, RAGConfig, WebKnowledgeCollector
        print("✅ 進階RAG模組導入成功")
    except ImportError as e:
        print(f"⚠️ 進階RAG模組導入失敗: {e}")
    
    try:
        from utils.enhanced_chatbot import EnhancedChatBot, ChatBot
        print("✅ 增強版chatbot模組導入成功")
    except ImportError as e:
        print(f"⚠️ 增強版chatbot模組導入失敗: {e}")
    
    try:
        from rag.core.simple_rag import SimpleRAGSystem
        print("✅ 簡化RAG模組導入成功")
    except ImportError as e:
        print(f"⚠️ 簡化RAG模組導入失敗: {e}")

def test_dependencies():
    """測試依賴包"""
    print("\n🔍 測試依賴包...")
    
    dependencies = [
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("sentence-transformers", "sentence_transformers"),
        ("faiss-cpu", "faiss"),
        ("openai", "openai")
    ]
    
    available_deps = []
    missing_deps = []
    
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name} 可用")
            available_deps.append(package_name)
        except ImportError:
            print(f"❌ {package_name} 不可用")
            missing_deps.append(package_name)
    
    if missing_deps:
        print(f"\n⚠️ 缺少依賴包: {', '.join(missing_deps)}")
        print("建議運行: pip install " + " ".join(missing_deps))
    
    return available_deps, missing_deps

async def test_rag_system():
    """測試RAG系統"""
    print("\n🔍 測試RAG系統...")
    
    try:
        from utils.advanced_rag import AdvancedRAGSystem, RAGConfig
        
        # 載入配置
        config = RAGConfig.load_config()
        print("✅ 配置載入成功")
        
        # 初始化RAG系統
        rag_system = AdvancedRAGSystem(config)
        print("✅ RAG系統初始化成功")
        
        # 測試檢索
        docs = rag_system.retrieve_documents("什麼是股票投資？", top_k=2)
        print(f"✅ 檢索到 {len(docs)} 個相關文檔")
        
        if docs:
            print(f"  - 最相關文檔: {docs[0]['title']}")
            print(f"  - 相似度分數: {docs[0].get('similarity_score', 0):.3f}")
        
        # 測試查詢
        result = await rag_system.query("投資股票有什麼風險？")
        print("✅ RAG查詢成功")
        print(f"  - 回答: {result['answer'][:100]}...")
        print(f"  - 信心度: {result['confidence']:.3f}")
        print(f"  - 檢索方法: {result.get('method', 'unknown')}")
        
        # 顯示統計信息
        stats = rag_system.get_statistics()
        print("✅ 系統統計:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG系統測試失敗: {e}")
        return False

async def test_enhanced_chatbot():
    """測試增強版chatbot"""
    print("\n🔍 測試增強版Chatbot...")
    
    try:
        from utils.enhanced_chatbot import EnhancedChatBot
        
        # 初始化
        chatbot = EnhancedChatBot()
        print("✅ 增強版chatbot初始化成功")
        
        # 測試各種查詢類型
        test_queries = [
            ("問候", "你好"),
            ("知識查詢", "什麼是本益比？"),
            ("投資概念", "技術分析是什麼？"),
            ("風險管理", "如何控制投資風險？")
        ]
        
        for query_type, query in test_queries:
            result = await chatbot.process_message(query)
            print(f"✅ {query_type}測試成功")
            print(f"  - 問題: {query}")
            print(f"  - 回答: {result['answer'][:80]}...")
            print(f"  - 信心度: {result.get('confidence', 0):.3f}")
            print(f"  - 回應時間: {result.get('response_time', 0):.3f}秒")
        
        # 測試系統狀態
        status = chatbot.get_system_status()
        print("✅ 系統狀態:")
        for key, value in status.items():
            if key != 'rag_statistics':
                print(f"  - {key}: {value}")
        
        # 測試對話歷史
        history = chatbot.get_conversation_history(limit=3)
        print(f"✅ 對話歷史: {len(history)} 條記錄")
        
        return True
        
    except Exception as e:
        print(f"❌ 增強版chatbot測試失敗: {e}")
        return False

async def test_knowledge_management():
    """測試知識管理"""
    print("\n🔍 測試知識管理...")
    
    try:
        from utils.enhanced_chatbot import EnhancedChatBot
        
        chatbot = EnhancedChatBot()
        
        # 添加新知識
        new_knowledge = [
            {
                "title": "加密貨幣投資",
                "content": "加密貨幣是基於區塊鏈技術的數位資產，具有去中心化特性。投資加密貨幣需要注意高波動性和監管風險。",
                "category": "數位資產",
                "source": "測試資料"
            }
        ]
        
        success = await chatbot.add_knowledge(new_knowledge)
        if success:
            print("✅ 新知識添加成功")
            
            # 測試新添加的知識
            result = await chatbot.process_message("什麼是加密貨幣？")
            print("✅ 新知識查詢測試:")
            print(f"  - 回答: {result['answer'][:80]}...")
        else:
            print("⚠️ 新知識添加失敗")
        
        return True
        
    except Exception as e:
        print(f"❌ 知識管理測試失敗: {e}")
        return False

def test_backward_compatibility():
    """測試向後兼容性"""
    print("\n🔍 測試向後兼容性...")
    
    try:
        from utils.enhanced_chatbot import ChatBot
        
        # 使用舊的同步介面
        chatbot = ChatBot()
        result = chatbot.query("什麼是股票？")
        print("✅ 同步介面測試成功")
        print(f"  - 回答: {result[:80]}...")
        
        # 測試知識搜索
        knowledge_results = chatbot.search_knowledge("投資")
        print(f"✅ 知識搜索測試: 找到 {len(knowledge_results)} 條結果")
        
        return True
        
    except Exception as e:
        print(f"❌ 向後兼容性測試失敗: {e}")
        return False

async def performance_test():
    """性能測試"""
    print("\n🔍 性能測試...")
    
    try:
        from utils.enhanced_chatbot import EnhancedChatBot
        import time
        
        chatbot = EnhancedChatBot()
        
        # 批次查詢測試
        queries = [
            "什麼是股票？",
            "如何分析公司財報？", 
            "技術分析有哪些指標？",
            "投資組合如何配置？",
            "什麼是ESG投資？"
        ]
        
        start_time = time.time()
        results = []
        
        for query in queries:
            result = await chatbot.process_message(query)
            results.append(result)
        
        total_time = time.time() - start_time
        avg_time = total_time / len(queries)
        
        print(f"✅ 批次查詢完成:")
        print(f"  - 總查詢數: {len(queries)}")
        print(f"  - 總時間: {total_time:.2f}秒")
        print(f"  - 平均時間: {avg_time:.2f}秒/查詢")
        
        # 分析回答品質
        confidence_scores = [r.get('confidence', 0) for r in results]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        print(f"  - 平均信心度: {avg_confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能測試失敗: {e}")
        return False

async def main():
    """主測試函數"""
    print("🚀 進階RAG系統完整測試")
    print("=" * 60)
    
    # 基礎測試
    test_imports()
    available_deps, missing_deps = test_dependencies()
    
    # 功能測試
    test_results = []
    
    tests = [
        ("RAG系統", test_rag_system),
        ("增強版Chatbot", test_enhanced_chatbot),
        ("知識管理", test_knowledge_management),
        ("向後兼容性", test_backward_compatibility),
        ("性能測試", performance_test)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                success = await test_func()
            else:
                success = test_func()
            test_results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name}執行失敗: {e}")
            test_results.append((test_name, False))
    
    # 總結報告
    print("\n" + "="*60)
    print("📊 測試總結報告")
    print("="*60)
    
    passed_tests = sum(1 for _, success in test_results if success)
    total_tests = len(test_results)
    
    print(f"測試通過率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"可用依賴: {len(available_deps)}/{len(available_deps)+len(missing_deps)}")
    
    print("\n詳細結果:")
    for test_name, success in test_results:
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"  {test_name}: {status}")
    
    if missing_deps:
        print(f"\n缺少依賴: {', '.join(missing_deps)}")
        print("建議安裝: pip install " + " ".join(missing_deps))
    
    # 建議
    print("\n💡 建議:")
    if passed_tests == total_tests:
        print("🎉 所有測試通過！系統運作正常。")
        if missing_deps:
            print("💡 安裝缺少的依賴包可以啟用更多功能。")
    elif passed_tests >= total_tests * 0.7:
        print("⚠️ 大部分功能正常，但有部分問題需要修復。")
    else:
        print("❌ 系統存在較多問題，建議檢查配置和依賴。")
    
    print("\n🔗 相關文件:")
    print("  - 安裝指南: RAG_整合指南.md")
    print("  - 配置文件: config/rag_config.json") 
    print("  - 自動安裝: python setup_advanced_rag.py")

if __name__ == "__main__":
    asyncio.run(main()) 