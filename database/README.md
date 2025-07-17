# 🗄️ Database 資料庫模組

台股財經網站的資料庫管理系統，提供完整的資料庫操作、模型定義和管理工具。

## 📁 目錄結構

```
database/
├── models.py           # 資料庫模型定義
├── manage.py           # 統一管理工具
├── utils/              # 資料庫工具
│   ├── db_viewer.py    # 資料庫查看工具
│   └── start.py        # 啟動腳本
├── backups/            # 資料庫備份目錄
└── README.md           # 本說明文檔
```

## 🏗️ 資料庫模型

### User（用戶模型）
- **用戶資料**：username, email, password_hash
- **個人資訊**：full_name, phone
- **會員等級**：free, premium, vip
- **時間戳記**：created_at, last_login
- **狀態**：is_active

### Watchlist（自選股模型）
- **關聯**：user_id (外鍵)
- **股票資訊**：stock_code, stock_name
- **追蹤資料**：added_price, notes
- **時間戳記**：created_at, updated_at

### SearchHistory（搜尋歷史）
- **關聯**：user_id (外鍵，可選)
- **搜尋資料**：stock_code, stock_name, search_price
- **追蹤資訊**：ip_address, user_agent
- **時間戳記**：created_at

### PriceAlert（價格提醒）
- **關聯**：user_id (外鍵)
- **股票資訊**：stock_code, stock_name
- **提醒設定**：alert_type, target_price
- **狀態**：is_active, is_triggered, triggered_at
- **備註**：notes

## 🛠 管理工具

### 統一管理腳本

```bash
# 運行資料庫管理工具
python database/manage.py
```

提供的功能：
1. **初始化資料庫** - 創建所有表格
2. **查看資料庫內容** - 瀏覽表格和資料
3. **備份資料庫** - 創建.db和.json備份
4. **重設資料庫** - 清空並重新初始化
5. **顯示統計資訊** - 用戶和資料統計

### 資料庫查看器

```bash
# 使用原始的資料庫查看器
python database/utils/db_viewer.py
```

功能：
- 顯示所有表格結構
- 查看表格內容
- 用戶資料查詢
- 會員系統統計

## 🚀 快速開始

### 1. 初始化資料庫

```bash
# 方法一：使用管理工具
python database/manage.py
# 選擇選項 1

# 方法二：直接初始化
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 2. 查看資料庫

```bash
# 使用統一管理工具
python database/manage.py
# 選擇選項 2

# 或使用專門的查看器
python database/utils/db_viewer.py
```

### 3. 備份資料庫

```bash
python database/manage.py
# 選擇選項 3
```

備份檔案會保存在 `database/backups/` 目錄中。

## 💻 程式化使用

### 導入模型

```python
from database import db, User, Watchlist, SearchHistory, PriceAlert

# 或者
from database.models import User, Watchlist
```

### 基本操作

```python
from app import app
from database import db, User

# 在應用上下文中操作
with app.app_context():
    # 查詢用戶
    user = User.query.filter_by(username='test').first()
    
    # 創建新用戶
    new_user = User(
        username='newuser',
        email='newuser@example.com',
        password_hash='hashed_password'
    )
    db.session.add(new_user)
    db.session.commit()
    
    # 查詢統計
    total_users = User.query.count()
    premium_users = User.query.filter_by(membership_level='premium').count()
```

### 自選股操作

```python
from database import Watchlist

with app.app_context():
    # 添加自選股
    watchlist = Watchlist(
        user_id=1,
        stock_code='2330',
        stock_name='台積電',
        added_price=500.0,
        notes='半導體龍頭股'
    )
    db.session.add(watchlist)
    db.session.commit()
    
    # 查詢用戶自選股
    user_stocks = Watchlist.query.filter_by(user_id=1).all()
```

## 🔧 資料庫配置

### 連接設定

資料庫配置在 `app.py` 中：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### 備份策略

- **自動備份**：每次重設前自動備份
- **手動備份**：使用管理工具或命令列
- **格式支援**：SQLite (.db) 和 JSON (.json) 格式

## 📊 資料庫統計

使用管理工具可以查看：
- 👥 用戶總數和會員等級分布
- 📈 自選股和搜尋記錄統計
- 🚨 價格提醒設定狀況
- 🆕 最近註冊用戶資訊

## 🐛 常見問題

### Q: 資料庫檔案在哪裡？
A: SQLite資料庫檔案位於 `instance/stock_app.db`

### Q: 如何遷移資料庫？
A: 使用備份功能匯出資料，然後在新環境中初始化並匯入

### Q: 如何修改模型？
A: 修改 `database/models.py`，然後重新初始化資料庫（會遺失資料）

### Q: 如何查看SQL查詢？
A: 設定 `app.config['SQLALCHEMY_ECHO'] = True` 可以看到所有SQL語句

## 🔄 版本更新

### v1.0.0 (當前版本)
- ✅ 完整的用戶系統
- ✅ 自選股管理
- ✅ 搜尋歷史追蹤
- ✅ 價格提醒功能
- ✅ 統一管理工具
- ✅ 備份與還原功能

---

**🗄️ 資料庫模組整合完成！**

現在您擁有一個完整的資料庫管理系統，支援：
- 📋 完整的模型定義
- 🛠 統一的管理工具
- 💾 自動備份功能
- 📊 詳細的統計資訊

立即開始使用：`python database/manage.py` 🚀 