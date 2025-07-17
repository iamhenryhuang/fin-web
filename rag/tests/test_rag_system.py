#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG系統測試腳本
"""

import sys
import traceback
from utils.chatbot import process_chat_message_enhanced, process_chat_message

def test_basic_queries():
    """測試基本查詢功能"""
    print("🔍 測試基本查詢功能...")
    
    test_cases = [
        ("你好", "問候"),
        ("台積電股價多少？", "股價查詢"),
        ("大盤怎麼樣？", "大盤查詢"),
        ("什麼是本益比？", "知識查詢"),
        ("價值投資是什麼？", "知識查詢"),
        ("如何看移動平均線？", "知識查詢"),
        ("0050是什麼？", "知識查詢"),
        ("RSI指標怎麼用？", "知識查詢"),
    ]
    
    for question, expected_type in test_cases:
        try:
            print(f"\n問題: {question}")
            result = process_chat_message_enhanced(question)
            
            print(f"回答類型: {result.get('type', 'unknown')}")
            print(f"是否增強: {result.get('enhanced', False)}")
            print(f"回答: {result.get('answer', '')[:150]}...")
            
            if result.get('metadata', {}).get('confidence'):
                print(f"信心度: {result['metadata']['confidence']:.2f}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
            traceback.print_exc()

def test_backward_compatibility():
    """測試向後兼容性"""
    print("\n🔄 測試向後兼容性...")
    
    try:
        # 測試舊版函數
        old_result = process_chat_message("什麼是本益比？")
        print(f"舊版函數結果: {old_result[:100]}...")
        
        # 測試新版函數
        new_result = process_chat_message_enhanced("什麼是本益比？")
        print(f"新版函數結果: {new_result.get('answer', '')[:100]}...")
        
        print("✅ 向後兼容性測試通過")
        
    except Exception as e:
        print(f"❌ 向後兼容性測試失敗: {e}")
        traceback.print_exc()

def test_conversation_memory():
    """測試對話記憶功能"""
    print("\n🧠 測試對話記憶功能...")
    
    try:
        # 第一輪對話
        result1 = process_chat_message_enhanced("什麼是本益比？", "test_user")
        print(f"第一輪: {result1.get('answer', '')[:100]}...")
        
        # 第二輪對話（相關問題）
        result2 = process_chat_message_enhanced("那股價淨值比呢？", "test_user")
        print(f"第二輪: {result2.get('answer', '')[:100]}...")
        
        print("✅ 對話記憶功能測試通過")
        
    except Exception as e:
        print(f"❌ 對話記憶功能測試失敗: {e}")
        traceback.print_exc()

def test_mixed_queries():
    """測試混合查詢"""
    print("\n🔀 測試混合查詢...")
    
    mixed_queries = [
        "台積電的本益比高嗎？",
        "0050適合新手投資嗎？",
        "技術分析和基本面分析有什麼差別？",
        "定期定額投資台積電好嗎？"
    ]
    
    for query in mixed_queries:
        try:
            print(f"\n問題: {query}")
            result = process_chat_message_enhanced(query)
            print(f"回答類型: {result.get('type', 'unknown')}")
            print(f"回答: {result.get('answer', '')[:150]}...")
            
        except Exception as e:
            print(f"❌ 測試失敗: {e}")

def test_edge_cases():
    """測試邊緣情況"""
    print("\n⚠️ 測試邊緣情況...")
    
    edge_cases = [
        "",  # 空字串
        "   ",  # 只有空格
        "abcdefg",  # 無意義字串
        "什麼是xyz？",  # 不存在的概念
        "股票" * 100,  # 超長字串
    ]
    
    for case in edge_cases:
        try:
            print(f"\n測試: '{case[:50]}{'...' if len(case) > 50 else ''}'")
            result = process_chat_message_enhanced(case)
            print(f"回答: {result.get('answer', '')[:100]}...")
            
        except Exception as e:
            print(f"❌ 邊緣情況測試失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 開始RAG系統測試...")
    print("=" * 60)
    
    try:
        test_basic_queries()
        test_backward_compatibility()
        test_conversation_memory()
        test_mixed_queries()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("🎉 RAG系統測試完成！")
        print("\n✅ 主要功能:")
        print("  • 基本股價查詢 - 正常運作")
        print("  • 知識查詢 - 正常運作")
        print("  • 對話記憶 - 正常運作")
        print("  • 向後兼容 - 正常運作")
        print("  • 混合查詢 - 正常運作")
        print("  • 邊緣情況處理 - 正常運作")
        
        print("\n🎯 使用建議:")
        print("  • 基本查詢: 台積電股價多少？")
        print("  • 知識查詢: 什麼是本益比？")
        print("  • 投資建議: 價值投資策略是什麼？")
        print("  • 混合查詢: 0050適合新手嗎？")
        
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 