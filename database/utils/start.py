#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台股財經網站啟動腳本
"""

import os
import sys

# 確保可以導入app模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, db

def main():
    """主啟動函數"""
    print("🚀 台股財經網站啟動中...")
    print("=" * 50)
    
    # 確保必要資料夾存在
    folders = ['static', 'cache', 'instance']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ 確保資料夾存在: {folder}")
    
    # 初始化資料庫
    try:
        with app.app_context():
            db.create_all()
            print("✅ 資料庫已初始化")
    except Exception as e:
        print(f"❌ 資料庫初始化錯誤: {e}")
        return
    
    # 顯示功能特色
    print("\n📊 功能特色:")
    print("  • 即時股價查詢")
    print("  • 會員系統")
    print("  • 自選股管理")
    print("  • REST API 服務")
    
    print("\n🌐 網址: http://127.0.0.1:5000")
    print("📚 API 文檔: http://127.0.0.1:5000")
    
    print("\n" + "=" * 50)
    print("🎉 啟動完成！按 Ctrl+C 停止服務")
    print("=" * 50)
    
    # 啟動應用程式
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 服務已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗: {e}")

if __name__ == "__main__":
    main() 