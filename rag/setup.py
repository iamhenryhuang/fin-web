#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG系統統一安裝腳本
支援多種安裝模式：基礎、進階、開發者模式
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """顯示安裝橫幅"""
    print("=" * 60)
    print("🤖 RAG智能問答系統安裝程序")
    print("=" * 60)
    print("支援多種安裝模式：")
    print("1. 基礎安裝 - 核心功能")
    print("2. 進階安裝 - 完整向量搜索")
    print("3. 開發者安裝 - 包含測試工具")
    print("=" * 60)

def check_python_version():
    """檢查Python版本"""
    print("🔍 檢查Python版本...")
    if sys.version_info < (3, 7, 0):
        print("❌ 需要Python 3.7+")
        print(f"當前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_dependencies(mode="basic"):
    """安裝依賴包"""
    print(f"📦 安裝依賴包 ({mode}模式)...")
    
    basic_packages = [
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "beautifulsoup4>=4.11.0"
    ]
    
    advanced_packages = [
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0", 
        "scikit-learn>=1.0.0",
        "openai>=1.0.0"
    ]
    
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "jupyter>=1.0.0"
    ]
    
    packages_to_install = basic_packages.copy()
    
    if mode in ["advanced", "dev"]:
        packages_to_install.extend(advanced_packages)
    
    if mode == "dev":
        packages_to_install.extend(dev_packages)
    
    try:
        for package in packages_to_install:
            print(f"安裝 {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
        print("✅ 依賴包安裝完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安裝失敗: {e}")
        return False

def create_directories():
    """創建目錄結構"""
    print("📁 創建目錄結構...")
    
    directories = [
        "../config",
        "../data", 
        "../data/knowledge",
        "../cache",
        "../cache/knowledge",
        "../cache/vectors",
        "../logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 創建目錄: {directory}")
    
    return True

def setup_configuration():
    """設置配置文件"""
    print("⚙️ 設置配置文件...")
    
    config_path = Path("../config/rag_config.json")
    
    if config_path.exists():
        print("配置文件已存在")
        choice = input("是否要重新設置？(y/n): ").lower()
        if choice != 'y':
            return True
    
    config = {
        "openai_api_key": "",
        "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
        "openai_model": "gpt-3.5-turbo",
        "max_context_length": 4000,
        "similarity_threshold": 0.7,
        "max_results": 5,
        "temperature": 0.7,
        "cache_enabled": True,
        "vector_cache_size": 1000
    }
    
    print("\n請設置RAG系統配置：")
    
    # API Key設置
    api_key = input("請輸入OpenAI API Key（可選，直接回車跳過）: ").strip()
    if api_key:
        config["openai_api_key"] = api_key
    
    # 模型選擇
    print("\n選擇嵌入模型：")
    print("1. paraphrase-multilingual-MiniLM-L12-v2 (推薦，支援中文)")
    print("2. all-MiniLM-L6-v2 (較快，主要英文)")
    print("3. 使用OpenAI embeddings (需要API key)")
    
    model_choice = input("請選擇 (1-3，默認1): ").strip()
    if model_choice == "2":
        config["embedding_model"] = "all-MiniLM-L6-v2"
    elif model_choice == "3":
        config["embedding_model"] = "openai"
    
    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置已保存到: {config_path}")
    return True

def run_setup_script(mode):
    """運行對應的安裝腳本"""
    print(f"🚀 運行{mode}模式安裝...")
    
    script_map = {
        "basic": "setup_rag.py",
        "advanced": "setup_advanced_rag.py"
    }
    
    if mode in script_map:
        script_path = Path("setup") / script_map[mode]
        if script_path.exists():
            try:
                subprocess.run([sys.executable, str(script_path)], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ 安裝腳本執行失敗: {e}")
                return False
    
    return True

def run_tests(mode):
    """運行測試"""
    print("🧪 運行系統測試...")
    
    test_scripts = {
        "basic": ["tests/test_simple_demo.py"],
        "advanced": ["tests/test_advanced_rag.py", "tests/quick_test.py"],
        "dev": ["tests/test_advanced_rag.py", "tests/test_lightweight_rag.py", "tests/quick_test.py"]
    }
    
    scripts_to_run = test_scripts.get(mode, ["tests/quick_test.py"])
    
    for script in scripts_to_run:
        script_path = Path(script)
        if script_path.exists():
            try:
                print(f"運行: {script}")
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {script} 測試通過")
                else:
                    print(f"⚠️ {script} 測試有警告")
            except subprocess.TimeoutExpired:
                print(f"⏰ {script} 測試超時")
            except Exception as e:
                print(f"❌ {script} 測試失敗: {e}")
    
    return True

def main():
    """主函數"""
    print_banner()
    
    # 選擇安裝模式
    print("\n請選擇安裝模式：")
    print("1. 基礎安裝 (推薦新手)")
    print("2. 進階安裝 (完整功能)")
    print("3. 開發者安裝 (包含測試工具)")
    
    choice = input("請選擇 (1-3，默認2): ").strip()
    
    mode_map = {
        "1": "basic",
        "2": "advanced", 
        "3": "dev"
    }
    
    mode = mode_map.get(choice, "advanced")
    print(f"\n🎯 選擇安裝模式: {mode}")
    
    # 執行安裝步驟
    steps = [
        ("檢查Python版本", lambda: check_python_version()),
        ("安裝依賴包", lambda: install_dependencies(mode)),
        ("創建目錄結構", lambda: create_directories()),
        ("設置配置", lambda: setup_configuration()),
        ("運行安裝腳本", lambda: run_setup_script(mode)),
        ("運行測試", lambda: run_tests(mode))
    ]
    
    print(f"\n🔄 開始{mode}模式安裝...")
    print("-" * 50)
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if not step_func():
                print(f"❌ {step_name}失敗")
                return False
        except Exception as e:
            print(f"❌ {step_name}失敗: {e}")
            return False
    
    # 安裝成功
    print("\n" + "=" * 60)
    print("🎉 RAG系統安裝完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 如果有OpenAI API key，請在 config/rag_config.json 中設置")
    print("2. 運行 python ../app.py 啟動主應用")
    print("3. 訪問 http://localhost:5000/chatbot 測試RAG功能")
    print("4. 運行 python tests/quick_test.py 快速測試")
    print("\n📚 詳細文檔請參考: README.md")
    print("🚀 開始探索您的智能RAG系統！")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 