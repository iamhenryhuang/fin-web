#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料庫管理工具
提供資料庫初始化、查看、備份等功能
"""

import os
import sys
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# 確保可以導入app模組
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 設置工作目錄為專案根目錄
os.chdir(parent_dir)

def init_database():
    """初始化資料庫"""
    print("🔧 初始化資料庫...")
    
    try:
        # 避免循環導入，直接導入必要的模組
        from database.models import db
        from flask import Flask
        
        # 創建最小化的Flask app配置
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        
        # 確保instance目錄存在
        os.makedirs('instance', exist_ok=True)
        
        with app.app_context():
            # 創建所有表格
            db.create_all()
            print("✅ 資料庫表格創建成功")
            
            # 顯示創建的表格
            tables = db.metadata.tables.keys()
            print(f"📊 創建的表格: {', '.join(tables)}")
            
        return True
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        return False

def view_database():
    """查看資料庫內容"""
    print("👀 查看資料庫內容...")
    
    db_path = Path('instance/stock_app.db')
    if not db_path.exists():
        print("❌ 資料庫檔案不存在，請先初始化資料庫")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 獲取所有表格
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 資料庫包含 {len(tables)} 個表格:")
        print("-" * 50)
        
        for table in tables:
            table_name = table['name']
            print(f"\n📋 表格: {table_name}")
            
            # 獲取表格結構
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("   欄位:")
            for col in columns:
                print(f"   - {col['name']} ({col['type']})")
            
            # 獲取記錄數量
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"   記錄數量: {count}")
            
            # 顯示最近的幾筆記錄
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                records = cursor.fetchall()
                print("   最近記錄:")
                for record in records:
                    print(f"   - {dict(record)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 查看資料庫失敗: {e}")
        return False

def backup_database():
    """備份資料庫"""
    print("💾 備份資料庫...")
    
    db_path = Path('instance/stock_app.db')
    if not db_path.exists():
        print("❌ 資料庫檔案不存在")
        return False
    
    try:
        # 創建備份目錄
        backup_dir = Path('database/backups')
        backup_dir.mkdir(exist_ok=True)
        
        # 生成備份檔名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"stock_app_backup_{timestamp}.db"
        
        # 複製資料庫檔案
        import shutil
        shutil.copy2(db_path, backup_file)
        
        print(f"✅ 資料庫已備份到: {backup_file}")
        
        # 也創建JSON格式的備份
        json_backup = backup_dir / f"stock_app_backup_{timestamp}.json"
        export_to_json(str(json_backup))
        
        return True
        
    except Exception as e:
        print(f"❌ 備份失敗: {e}")
        return False

def export_to_json(json_file):
    """匯出資料庫到JSON格式"""
    try:
        conn = sqlite3.connect('instance/stock_app.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        data = {}
        
        # 獲取所有表格
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table['name']
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            data[table_name] = []
            for record in records:
                # 轉換Row對象為字典，處理datetime對象
                record_dict = {}
                for key in record.keys():
                    value = record[key]
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    record_dict[key] = value
                data[table_name].append(record_dict)
        
        # 寫入JSON檔案
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON備份已創建: {json_file}")
        conn.close()
        
    except Exception as e:
        print(f"❌ JSON匯出失敗: {e}")

def reset_database():
    """重設資料庫"""
    print("⚠️ 重設資料庫...")
    
    confirm = input("這將刪除所有資料，確定要繼續嗎？(y/N): ").lower()
    if confirm != 'y':
        print("❌ 操作已取消")
        return False
    
    try:
        # 備份現有資料庫
        backup_database()
        
        # 刪除資料庫檔案
        db_path = Path('instance/stock_app.db')
        if db_path.exists():
            db_path.unlink()
            print("✅ 舊資料庫已刪除")
        
        # 重新初始化
        init_database()
        print("✅ 資料庫已重設")
        
        return True
        
    except Exception as e:
        print(f"❌ 重設失敗: {e}")
        return False

def show_stats():
    """顯示資料庫統計資訊"""
    print("📊 資料庫統計資訊...")
    
    db_path = Path('instance/stock_app.db')
    if not db_path.exists():
        print("❌ 資料庫檔案不存在")
        return False
    
    try:
        # 避免循環導入，直接導入必要的模組
        from database.models import db, User, Watchlist, SearchHistory, PriceAlert
        from flask import Flask
        
        # 創建最小化的Flask app配置  
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        
        with app.app_context():
            print("-" * 50)
            print(f"👥 用戶總數: {User.query.count()}")
            print(f"📈 自選股總數: {Watchlist.query.count()}")
            print(f"🔍 搜尋記錄總數: {SearchHistory.query.count()}")
            print(f"🚨 價格提醒總數: {PriceAlert.query.count()}")
            
            # 會員等級統計
            print("\n👑 會員等級分布:")
            for level in ['free', 'premium', 'vip']:
                count = User.query.filter_by(membership_level=level).count()
                print(f"   {level}: {count} 人")
            
            # 最近註冊用戶
            recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
            print(f"\n🆕 最近註冊用戶:")
            for user in recent_users:
                print(f"   {user.username} ({user.created_at.strftime('%Y-%m-%d %H:%M')})")
            
            print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 統計資訊獲取失敗: {e}")
        return False

def main():
    """主函數"""
    print("🗄️ 資料庫管理工具")
    print("=" * 50)
    
    while True:
        print("\n請選擇操作:")
        print("1. 初始化資料庫")
        print("2. 查看資料庫內容")
        print("3. 備份資料庫")
        print("4. 重設資料庫")
        print("5. 顯示統計資訊")
        print("0. 退出")
        
        choice = input("\n請輸入選項 (0-5): ").strip()
        
        if choice == '0':
            print("👋 再見！")
            break
        elif choice == '1':
            init_database()
        elif choice == '2':
            view_database()
        elif choice == '3':
            backup_database()
        elif choice == '4':
            reset_database()
        elif choice == '5':
            show_stats()
        else:
            print("❌ 無效選項，請重新輸入")

if __name__ == "__main__":
    main() 