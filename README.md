# 台股財經網站

🚀 **現代化的台股查詢系統**

提供即時股價查詢、會員管理和投資組合追蹤的一站式金融平台。

## ✨ 核心功能

### 📈 股票查詢系統
- 即時股價（多資料來源備援）
- 大盤資訊與熱門股票
- 技術圖表（MA/RSI/MACD）
- 圖表資料支援查詢天數 1–180 天
- 智能快取：5 分鐘快取提升效能

### 🛠️ 投資工具
- 股息計算器（支援年/半年/季/月配與再投入）`/tools/dividend`
- 技術分析（MA、RSI、MACD）`/tools/ta`
- 資產配置（風險等級、自選資產、年期/每月投入、投組指標與期末估算）`/tools/allocation`
- 定期定額試算（投入/頻率/年化報酬）`/tools/dca`
- 股價預測（簡易趨勢外推，無 ML 依賴）`/tools/ai`

### 👥 會員系統
- 等級：免費/付費/VIP
- 自選股管理與搜尋歷史
- 個人儀表板

### 🎨 UI/UX
- 深/淺色主題切換、行動底部導覽
- 表格緊湊模式、數字對齊、顏色標示

## 🚀 快速開始

### 系統需求
- Python 3.8+
- 256MB+ 可用記憶體

### 安裝步驟

```bash
# 1. 複製專案
git clone [repository-url]
cd financial_web

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 啟動應用
python app.py
```

### 訪問網站
- 🏠 http://localhost:5000 - 首頁
- 📊 http://localhost:5000/stock?code=2330 - 股票查詢
- 👤 http://localhost:5000/login - 會員登入

## 📁 專案結構

```
financial_web/
│
├── 📱 Flask 核心應用
│   ├── app.py              # 主應用程式
│   ├── forms.py            # 表單驗證
│   ├── models.py           # 資料模型
│   └── requirements.txt    # 依賴需求
│
├── 💾 資料庫系統
│   ├── database/           # 資料庫模組
│   │   ├── __init__.py    # 資料庫初始化
│   │   └── models.py      # 資料模型定義
│
├── 🛠️ 工具模組
│   ├── utils/
│   │   ├── twse.py        # 台股資料API
│   │   └── __init__.py
│
├── 📊 配置與資料
│   └── cache/             # 快取文件
│
├── 🌐 前端資源
│   ├── templates/         # Jinja2 模板
│   │   ├── home.html      # 首頁
│   │   ├── stock.html     # 股票頁面
│   │   ├── auth/          # 會員系統
│   │   ├── member/        # 會員功能
│   │   └── tools/         # 投資工具（dividend, ta, allocation, dca, ai）
│   └── static/            # 靜態資源
│       ├── css/           # 樣式表
│       ├── js/            # JavaScript
│       └── images/        # 圖片資源
│
└── 📋 其他文件
    ├── README.md          # 專案說明
    ├── .gitignore         # Git 忽略清單
```

## 🌐 API 端點

| 端點 | 說明 | 權限 |
|------|------|------|
| `/` | 首頁，股票搜尋 | 公開 |
| `/stock?code=XXXX` | 個股資訊頁面 | 公開 |
| `/login` | 會員登入 | 公開 |
| `/register` | 會員註冊 | 公開 |
| `/dashboard` | 會員儀表板 | 會員 |
| `/watchlist` | 自選股管理 | 會員 |
| `/api/stock/<code>` | 股票資料 API | 公開 |
| `/api/stock/<code>/chart?days=N` | 圖表資料（N: 1–180） | 公開 |
| `/api/market` | 大盤資料 API | 公開 |
| `/api/popular` | 熱門股票清單 | 公開 |

### API 使用範例

```bash
# 獲取個股資訊
curl http://localhost:5000/api/stock/2330

# 獲取大盤資訊
curl http://localhost:5000/api/market

# 獲取熱門股票
curl http://localhost:5000/api/popular

# 獲取 90 天圖表資料
curl "http://localhost:5000/api/stock/2330/chart?days=90"
```

## ⚙️ 開發設定

### 開發環境依賴

```bash
# 基礎套件
pip install -r requirements.txt

# 開發工具（可選）
pip install pytest flask-testing
```

### 資料庫設定

應用程式會自動創建 SQLite 資料庫文件。如需使用其他資料庫：

```python
# 在 app.py 中修改
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url'
```

### 環境變數

創建 `.env` 文件：

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///stock_app.db
```

## 🧪 測試

```bash
# 執行測試
python -m pytest

# 功能測試
python -c "from utils.twse import get_stock_basic_info; print(get_stock_basic_info('2330'))"
```

## 📱 功能特色

### 即時資料
- 台股開盤時間即時更新股價
- 智能快取機制優化查詢速度
- 多重資料來源確保資料可靠性

### 使用者體驗
- 響應式設計，支援手機、平板、桌機
- 直觀的搜尋介面
- 快速導航和操作

## 📚 技術文檔

- 📖 [Flask 官方文檔](https://flask.palletsprojects.com/)
- 🗄️ [SQLAlchemy 文檔](https://sqlalchemy.org/)
- 🎨 [Bootstrap 文檔](https://getbootstrap.com/)

## 📄 授權

本專案使用 MIT 授權條款。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

📧 如有問題或建議，請聯繫開發團隊。