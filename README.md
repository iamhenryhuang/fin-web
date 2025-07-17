# 台股財經網站 + RAG智能問答系統

現代化的台股查詢系統，整合 RAG 智能問答功能，提供即時股價查詢、財經知識問答和會員管理。

## ⚡ 快速開始

```bash
# 1. 安裝基礎依賴
pip install -r requirements.txt

# 2. 初始化資料庫
python database/manage.py
# 選擇選項 1

# 3. 啟動應用
python app.py

# 4. 訪問系統
# http://localhost:5000 - 主頁面
# http://localhost:5000/chatbot - RAG問答
```

## 🎯 核心功能

### 📈 股票查詢
- **即時股價**：台股個股、ETF 即時價格查詢
- **大盤資訊**：市場指數和概況
- **自選股**：會員專屬收藏管理
- **搜尋歷史**：查詢記錄追蹤

### 🤖 RAG智能問答
- **財經知識**：「什麼是本益比？」「價值投資策略」
- **即時股價**：「台積電今天股價？」「大盤表現如何？」
- **技術分析**：「移動平均線怎麼看？」「RSI指標用法」
- **複合查詢**：結合即時資料和知識解答

### 👥 會員系統
- **三層等級**：免費/付費/VIP
- **個人化**：自選股、搜尋歷史
- **安全管理**：註冊、登入、密碼修改

## 📁 專案結構

```
financial_web/
├── app.py              # 主應用程式
├── forms.py            # 表單定義
├── rag/                # RAG智能問答系統
│   ├── core/           # 核心實現
│   ├── setup/          # 安裝腳本
│   └── tests/          # 測試工具
├── database/           # 資料庫管理
│   ├── models.py       # 資料模型
│   ├── manage.py       # 管理工具
│   └── utils/          # 工具腳本
├── utils/              # 工具函數
│   └── twse.py         # 台股API接口
├── templates/          # HTML模板
├── static/             # CSS/JS資源
├── config/             # 配置檔案
└── instance/           # SQLite資料庫
```

## 🔧 進階設定

### RAG系統安裝
```bash
cd rag
python setup.py  # 選擇進階安裝模式
```

### 資料庫管理
```bash
python database/manage.py
# 1. 初始化資料庫
# 2. 查看資料內容
# 3. 備份資料庫
# 5. 統計資訊
```

### OpenAI API 設定（可選）
編輯 `config/rag_config.json`：
```json
{
  "openai_api_key": "your-api-key",
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
}
```

## 🌐 主要頁面

- **首頁** (`/`) - 股票搜尋、大盤資訊
- **個股頁面** (`/stock/<code>`) - 詳細股票資訊
- **聊天機器人** (`/chatbot`) - RAG智能問答
- **會員區** (`/member/`) - 個人化功能
- **登入註冊** (`/auth/`) - 用戶管理

## 🛠 技術架構

- **後端**：Flask + SQLAlchemy
- **前端**：Bootstrap 5 + Vanilla JS
- **資料庫**：SQLite
- **RAG系統**：sentence-transformers + FAISS
- **股價API**：Yahoo Finance

## 📦 依賴包

核心依賴：
```
Flask>=2.3.0
SQLAlchemy>=2.0.0
requests>=2.28.0
pandas>=1.5.0
```

RAG依賴（可選）：
```
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
openai>=1.0.0
```

## 🧪 測試功能

```bash
# RAG系統測試
python rag/tests/quick_test.py

# 資料庫功能測試
python database/manage.py  # 選項5查看統計
```

## 🎨 功能展示

### 股票查詢範例
- 輸入：`2330` → 顯示台積電完整資訊
- 輸入：`0050` → 顯示台灣50 ETF資訊

### RAG問答範例
- 「台積電股價多少？」→ 即時股價 + 公司介紹
- 「什麼是技術分析？」→ 專業知識解答
- 「如何投資ETF？」→ 投資策略指導

## 📝 注意事項

- 股價資料有5分鐘快取延遲
- RAG系統首次啟動需下載模型（約500MB）
- SQLite資料庫檔案位於 `instance/` 目錄
- 建議Python 3.8+環境

## 📚 詳細文檔

- [快速開始指南](QUICK_START.md)
- [RAG系統說明](rag/README.md)
- [資料庫管理](database/README.md)

---

**🚀 立即體驗您的智能財經系統！** 
=======
# 台股財經網站

一個現代化的台股即時查詢系統，提供股票價格查詢、大盤資訊、會員系統和 REST API 服務。

## 🚀 功能特色

- **即時股價查詢**：支援台股個股、ETF 查詢
- **大盤資訊**：顯示市場概況和指數資料
- **會員系統**：三層會員制度（免費/付費/VIP）
- **自選股管理**：會員專屬自選股功能
- **搜尋歷史**：自動記錄查詢歷史
- **現代化介面**：使用 Bootstrap 5 響應式設計
- **REST API**：提供 JSON 格式的資料接口
- **多重資料來源**：Yahoo Finance API 為主，確保資料穩定性
- **智能快取**：5分鐘快取機制，提升查詢效能

## 📱 介面預覽

### 首頁
- 股票搜尋功能
- 大盤指數資訊
- 熱門股票快速連結

### 個股頁面
- 完整股票資訊展示
- 即時價格和漲跌幅
- 交易量和基本資料
- 加入自選股功能（會員專屬）

### 會員系統
- **登入/註冊**：安全的用戶認證
- **會員控制台**：個人化儀表板
- **自選股管理**：即時價格追蹤
- **個人資料**：資料編輯和會員狀態
- **搜尋歷史**：查詢記錄管理

## 🛠 技術架構

- **後端**：Python Flask + Flask-Login + Flask-SQLAlchemy
- **前端**：Bootstrap 5 + JavaScript
- **資料庫**：SQLite + SQLAlchemy 2.0
- **資料來源**：Yahoo Finance API
- **快取系統**：檔案快取（5分鐘）
- **樣式**：自定義 CSS + Bootstrap Icons

## 📂 專案結構

```
financial_web/
├── app.py                 # Flask 主應用程式
├── models.py              # 資料庫模型
├── forms.py               # 表單類別
├── db_viewer.py           # 資料庫查看工具
├── utils/
│   └── twse.py           # 股票資料抓取模組
├── templates/
│   ├── home.html         # 首頁模板
│   ├── stock.html        # 個股頁面模板
│   ├── auth/
│   │   ├── login.html    # 登入頁面
│   │   └── register.html # 註冊頁面
│   ├── member/
│   │   ├── dashboard.html # 會員控制台
│   │   ├── watchlist.html # 自選股管理
│   │   ├── profile.html   # 個人資料
│   │   └── change_password.html # 修改密碼
│   └── error.html        # 錯誤頁面模板
├── static/
│   └── style.css         # 自定義樣式
├── cache/                # 快取資料夾
├── instance/             # 資料庫檔案
└── README.md             # 說明文件
```

## 🚀 快速開始

### 1. 安裝相依套件

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms email-validator requests pandas werkzeug
```

### 2. 初始化資料庫

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 3. 啟動應用程式

```bash
python app.py
```

### 4. 開啟瀏覽器
```
http://127.0.0.1:5000
```
---

**免責聲明**：本系統提供的股價資訊僅供參考，不構成投資建議。投資有風險，請謹慎評估後做出決策。 
