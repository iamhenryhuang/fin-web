# 台股財經網站

🚀 **現代化的台股查詢與投資分析平台**

提供即時股價查詢、技術分析工具、會員管理和投資組合追蹤的一站式台股金融平台。

## ✨ 核心功能

### 📈 股票查詢系統
- **即時股價資料**：多資料來源備援（證交所、Yahoo Finance）
- **大盤資訊**：台股加權指數即時資料與熱門股票
- **圖表資料**：支援 1-30 天歷史價格查詢
- **智能快取**：5 分鐘快取機制提升查詢效能
- **股票名稱搜尋**：支援中文名稱與代碼查詢

### 🛠️ 投資分析工具
- **股息計算器** (`/tools/dividend`) - 支援年/半年/季/月配息與股息再投入計算
- **技術分析** (`/tools/ta`) - MA、RSI、MACD 技術指標分析
- **智能選股** (`/tools/screener`) - 基於技術指標的股票篩選系統
- **資產配置** (`/tools/allocation`) - 風險等級評估與投資組合配置
- **定期定額** (`/tools/dca`) - 定期定額投資試算

### 👥 會員系統
- **會員等級**：免費/付費/VIP 三級制度
- **自選股管理**：個人化股票追蹤與備註
- **搜尋歷史**：記錄查詢歷史便於回顧
- **價格提醒**：付費會員專享股價警示功能
- **個人儀表板**：整合個人投資資訊

### 🎨 使用者介面
- **Bloomberg 風格**：專業金融網站設計風格
- **響應式設計**：支援手機、平板、桌機多裝置
- **專業數據展示**：優化的財務數據呈現

## 🚀 快速開始

### 系統需求
- Python 3.8+

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
- 📊 http://localhost:5000/stock?code=2330 - 股票查詢（台積電）
- 👤 http://localhost:5000/login - 會員登入

## 📁 專案結構

```
financial_web/
│
├── 📱 核心應用
│   ├── app.py                    # Flask 主應用程式
│   ├── forms.py                  # WTForms 表單驗證
│   ├── models.py                 # 資料模型（與database重複，向後兼容）
│   └── requirements.txt          # Python 依賴套件
│
├── 🗄️ 資料庫系統
│   ├── database/
│   │   ├── __init__.py          # 資料庫模組初始化
│   │   ├── models.py            # SQLAlchemy 資料模型
│   │   ├── manage.py            # 資料庫管理工具
│   │   ├── README.md            # 資料庫文檔
│   │   └── utils/               # 資料庫工具
│   │       ├── db_viewer.py     # 資料庫檢視器
│   │       └── start.py         # 啟動工具
│   └── backups/                 # 資料庫備份目錄
│
├── 🛠️ 工具模組
│   └── utils/
│       ├── twse.py              # 台股資料 API 整合
│       ├── news.py              # Yahoo 財經新聞爬蟲
│       └── stock_screener.py    # 股票選股分析引擎
│
├── 💾 資料與快取
│   ├── cache/                   # API 資料快取（JSON 格式）
│   └── instance/                # Flask 實例資料
│       ├── stock_app.db         # SQLite 資料庫
│       └── ai_models/           # AI 模型檔案
│
├── 🌐 前端資源
│   ├── templates/               # Jinja2 HTML 模板
│   │   ├── home.html           # 首頁模板
│   │   ├── stock.html          # 個股頁面模板
│   │   ├── error.html          # 錯誤頁面模板
│   │   ├── auth/               # 會員認證模板
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── member/             # 會員功能模板
│   │   │   ├── dashboard.html
│   │   │   ├── profile.html
│   │   │   ├── watchlist.html
│   │   │   └── change_password.html
│   │   ├── tools/              # 投資工具模板
│   │   │   ├── dividend_calculator.html
│   │   │   ├── ta.html
│   │   │   ├── screener.html
│   │   │   ├── allocation.html
│   │   │   ├── dca.html
│   │   │   └── ai.html
│   │   └── layouts/            # 佈局模板
│   └── static/                 # 靜態資源
│       └── main.css            # Bloomberg風格主要樣式檔案
│
├── 📄 配置與文檔
│   └── README.md                       # 專案說明文檔
│
└── 🔧 開發工具
    ├── db_viewer.py            # 資料庫檢視工具（根目錄）
    └── .env.example            # 環境變數範例
```

## 🌐 API 端點

### 公開 API
| 端點 | 說明 | 參數 |
|------|------|------|
| `/` | 首頁，股票搜尋與大盤資訊 | - |
| `/stock` | 個股資訊頁面 | `code`: 股票代碼 |
| `/search` | 股票搜尋重導向 | `q`: 搜尋關鍵字 |

### 會員功能
| 端點 | 說明 | 權限 |
|------|------|------|
| `/login` | 會員登入 | 公開 |
| `/register` | 會員註冊 | 公開 |
| `/logout` | 會員登出 | 會員 |
| `/dashboard` | 會員儀表板 | 會員 |
| `/profile` | 個人資料管理 | 會員 |
| `/change_password` | 修改密碼 | 會員 |
| `/watchlist` | 自選股管理 | 會員 |

### 投資工具
| 端點 | 說明 | 功能 |
|------|------|------|
| `/tools/dividend` | 股息計算器 | 股息與再投入計算 |
| `/tools/ta` | 技術分析 | 技術指標分析 |
| `/tools/screener` | 智能選股 | 基於指標的股票篩選 |
| `/tools/allocation` | 資產配置 | 投資組合配置建議 |
| `/tools/dca` | 定期定額 | 定期投資試算 |
| `/tools/ai` | AI 預測 | 股價趨勢預測 |

### REST API
| 端點 | 說明 | 回應格式 |
|------|------|----------|
| `/api/stock/<code>` | 個股即時資料 | JSON |
| `/api/stock/<code>/chart` | 股票圖表資料 | JSON (`days` 參數：1-30) |
| `/api/market` | 大盤即時資料 | JSON |
| `/api/popular` | 熱門股票清單 | JSON |
| `/api/screener` | 股票篩選 | JSON (POST) |
| `/api/screener/strategies` | 預設選股策略 | JSON |
| `/api/watchlist/add` | 加入自選股 | JSON (POST, 需登入) |

### API 使用範例

```bash
# 獲取台積電股票資訊
curl http://localhost:5000/api/stock/2330

# 獲取大盤資訊
curl http://localhost:5000/api/market

# 獲取熱門股票清單
curl http://localhost:5000/api/popular

# 獲取台積電 7 天圖表資料
curl "http://localhost:5000/api/stock/2330/chart?days=7"

# 獲取預設選股策略
curl http://localhost:5000/api/screener/strategies
```

## ⚙️ 技術架構

### 後端技術
- **Flask 2.3+**：Web 框架
- **SQLAlchemy 3.0+**：ORM 資料庫操作
- **Flask-Login**：使用者認證
- **Flask-WTF**：表單處理與驗證
- **SQLite**：輕量級資料庫
- **Requests**：HTTP 請求處理
- **BeautifulSoup4**：網頁解析

### 前端技術
- **Jinja2**：模板引擎
- **Bloomberg CSS Theme**：專業金融介面
- **響應式設計**：支援多裝置
- **JavaScript**：互動功能

### 資料來源
- **證交所即時 API**：官方股價資料
- **Yahoo Finance API**：備用資料來源
- **新聞爬蟲**：財經新聞整合

## 🗄️ 資料庫結構

### 資料表說明
- **users**：使用者資料與會員等級
- **watchlists**：自選股管理
- **search_history**：搜尋歷史記錄

### 資料庫管理
```bash
# 初始化資料庫
python database/manage.py

# 查看資料庫內容
python db_viewer.py

# 備份資料庫（自動產生 JSON 和 DB 檔案）
python database/manage.py  # 選擇備份選項
```

## 🧪 測試與除錯

```bash
# 功能測試
python -c "from utils.twse import get_stock_basic_info; print(get_stock_basic_info('2330'))"

# 新聞模組測試
python -c "from utils.news import get_yahoo_stock_top_news; print(get_yahoo_stock_top_news(3))"

# 選股器測試
python -c "from utils.stock_screener import StockScreener; s = StockScreener(); print(s.analyze_stock('2330'))"
```

## 📦 部署說明

### 環境變數設定
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///stock_app.db
FLASK_ENV=production
```

### 生產環境部署
```bash
# 使用 gunicorn
pip install gunicorn
gunicorn app:app -w 4 -b 0.0.0.0:5000

# 或使用 Flask 內建伺服器（僅開發用）
python app.py
```

## 📱 功能特色

### 即時資料處理
- 台股開盤時間即時更新股價資料
- 多重資料來源容錯機制
- 智能快取系統優化查詢效能
- 支援 4-6 位數股票代碼

### 投資分析工具
- 技術指標計算（RSI、MACD、移動平均）
- 股息再投入複利計算
- 智能選股演算法
- 投資組合風險評估

### 使用者體驗
- Bloomberg 專業金融介面設計
- 響應式設計支援多裝置
- 會員分級功能管理
- 直觀的搜尋與導航介面

## 📄 授權

本專案使用 MIT 授權條款。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

📧 如有問題或建議，請聯繫開發團隊。