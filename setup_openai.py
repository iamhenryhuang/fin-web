#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI API Key 設定工具
快速設定語言模型整合
"""

import json
import os
from pathlib import Path

def setup_openai_key():
    """設定 OpenAI API Key"""
    print("🤖 語言模型設定工具")
    print("=" * 50)
    
    # 檢查配置文件
    config_file = Path("config/rag_config.json")
    if not config_file.exists():
        print("❌ 找不到配置文件: config/rag_config.json")
        return False
    
    # 讀取現有配置
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("目前配置狀態：")
    current_key = config.get('openai_api_key', '')
    if current_key and current_key != 'YOUR_OPENAI_API_KEY_HERE':
        print(f"✅ OpenAI API Key: {current_key[:10]}...{current_key[-4:] if len(current_key) > 14 else current_key}")
    else:
        print("⚠️ OpenAI API Key: 未設定")
    
    print(f"🔧 語言模型: {config.get('openai_model', 'gpt-3.5-turbo')}")
    print(f"🔄 智能回退: {'啟用' if config.get('enable_fallback', True) else '停用'}")
    
    # 詢問是否要設定/更新 API key
    print("\n" + "=" * 50)
    print("選項：")
    print("1. 設定/更新 OpenAI API Key")
    print("2. 測試目前配置")
    print("3. 顯示獲取 API Key 指南")
    print("4. 退出")
    
    choice = input("\n請選擇 (1-4): ").strip()
    
    if choice == "1":
        return setup_api_key(config, config_file)
    elif choice == "2":
        return test_configuration(config)
    elif choice == "3":
        show_api_guide()
        return True
    else:
        print("👋 退出設定工具")
        return True

def setup_api_key(config, config_file):
    """設定 API Key"""
    print("\n🔑 OpenAI API Key 設定")
    print("-" * 30)
    
    # 獲取 API key
    api_key = input("請輸入您的 OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ API Key 不能為空")
        return False
    
    if len(api_key) < 20:
        print("❌ API Key 格式似乎不正確（長度太短）")
        return False
    
    # 更新配置
    config['openai_api_key'] = api_key
    config['enable_openai'] = True
    
    # 保存配置
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ API Key 設定成功！")
        print("🚀 語言模型整合已啟用")
        
        # 設定環境變數（當前會話）
        os.environ['OPENAI_API_KEY'] = api_key
        print("🔧 環境變數已設定")
        
        return True
        
    except Exception as e:
        print(f"❌ 保存配置失敗: {e}")
        return False

def test_configuration(config):
    """測試配置"""
    print("\n🧪 測試配置...")
    print("-" * 30)
    
    # 檢查基本配置
    api_key = config.get('openai_api_key', '')
    if not api_key or api_key == 'YOUR_OPENAI_API_KEY_HERE':
        print("❌ API Key 未設定")
        return False
    
    print("✅ API Key 已設定")
    
    # 測試 OpenAI 連接
    try:
        import openai
        
        # 設定 API key
        openai.api_key = api_key
        
        # 測試簡單請求
        print("🔄 測試 OpenAI 連接...")
        
                 from openai import OpenAI
         client = OpenAI(api_key=api_key)
         
         response = client.chat.completions.create(
             model=config.get('openai_model', 'gpt-3.5-turbo'),
             messages=[
                 {"role": "user", "content": "Hello, this is a test. Please respond with 'Test successful'."}
             ],
             max_tokens=50
         )
        
        answer = response.choices[0].message.content.strip()
        print(f"✅ OpenAI 回應: {answer}")
        print("🎉 語言模型整合測試成功！")
        return True
        
    except ImportError:
        print("❌ 未安裝 openai 套件")
        print("請執行: pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI 連接失敗: {e}")
        print("請檢查 API Key 是否正確，以及網路連接")
        return False

def show_api_guide():
    """顯示 API Key 獲取指南"""
    print("\n📖 OpenAI API Key 獲取指南")
    print("=" * 50)
    print("1. 前往 OpenAI 官網：https://platform.openai.com/")
    print("2. 註冊或登入您的帳號")
    print("3. 進入 API Keys 頁面：https://platform.openai.com/api-keys")
    print("4. 點選 'Create new secret key'")
    print("5. 複製產生的 API key（以 sk- 開頭）")
    print("6. 將 API key 貼到本設定工具中")
    print("\n💡 注意事項：")
    print("• API key 只會顯示一次，請妥善保存")
    print("• 使用 API 會產生費用，請參考 OpenAI 定價")
    print("• 建議設定使用額度限制")
    print("• 如果沒有 API key，系統會使用本地模板回答")

def main():
    """主函數"""
    try:
        setup_openai_key()
    except KeyboardInterrupt:
        print("\n\n👋 使用者中斷，退出設定")
    except Exception as e:
        print(f"\n❌ 設定過程發生錯誤: {e}")

if __name__ == "__main__":
    main() 