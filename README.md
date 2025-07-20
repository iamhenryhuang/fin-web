# 台股財經網站 + RAG智能問答系統

🚀 **現代化的台股查詢系統，整合 RAG 智能問答功能**

提供即時股價查詢、財經知識問答、會員管理和智能分析的一站式金融平台。

## ✨ 核心功能

### 📈 股票查詢系統
- **即時股價**：台股個股、ETF 即時價格查詢
- **大盤資訊**：市場指數和概況資料
- **熱門股票**：快速訪問熱門個股
- **技術圖表**：價格走勢和技術指標
- **智能快取**：5分鐘快取機制，提升查詢效能

### 🤖 RAG智能問答
- **財經知識**：「什麼是本益比？」「價值投資策略如何運用？」
- **即時股價**：「台積電今天股價？」「大盤表現如何？」
- **技術分析**：「移動平均線怎麼看？」「RSI指標使用方法」
- **複合查詢**：結合即時資料和專業知識的綜合解答
- **多模式支援**：OpenAI GPT + 本地嵌入模型雙重保障

### 👥 會員系統
- **三層等級**：免費/付費/VIP 差異化服務
- **自選股管理**：個人化投資組合追蹤
- **搜尋歷史**：查詢記錄自動保存
- **價格警報**：股價變動即時通知
- **個人儀表板**：一站式資訊中心

## 🚀 快速開始

### 環境需求
- Python 3.8+
- pip 包管理器
- 512MB+ 可用記憶體（RAG模型需求）

### 一鍵啟動
```bash
# 1. 克隆專案
git clone <your-repo-url>
cd financial_web

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 初始化資料庫
python database/manage.py
# 選擇選項 1 進行初始化

# 4. 啟動應用
python app.py

# 5. 開啟瀏覽器訪問
# http://localhost:5000 - 主頁面
# http://localhost:5000/chatbot - RAG智能問答
# http://localhost:5000/member/dashboard - 會員中心
```

### 可選配置
```bash
# 設定 OpenAI API（增強RAG功能）
python setup_openai.py

# RAG系統進階設定
cd rag
python setup.py  # 選擇進階安裝模式
```

## 📁 專案架構

```
financial_web/
├── 🌟 核心應用
│   ├── app.py              # Flask 主應用程式
│   ├── forms.py            # 表單定義和驗證
│   ├── models.py           # 資料庫模型
│   └── setup_openai.py     # OpenAI API 設定工具
│
├── 🤖 RAG智能問答系統
│   ├── core/               # 核心實現
│   │   ├── chatbot.py      # 聊天機器人邏輯
│   │   ├── enhanced_chatbot.py # 增強版聊天機器人
│   │   ├── rag_system.py   # RAG系統核心
│   │   └── knowledge_initializer.py # 知識庫初始化
│   ├── setup/              # 安裝和配置腳本
│   ├── tests/              # 測試工具
│   └── docs/               # RAG系統文檔
│
├── 🗄️ 資料庫管理
│   ├── __init__.py         # 資料庫初始化
│   ├── models.py           # 資料模型定義
│   ├── manage.py           # 資料庫管理工具
│   ├── utils/              # 資料庫工具
│   └── backups/            # 自動備份
│
├── 🔧 工具和服務
│   ├── utils/
│   │   ├── twse.py         # 台股API接口
│   │   └── chatbot.py      # 聊天機器人工具
│   ├── config/             # 配置檔案
│   │   └── rag_config.json # RAG系統配置
│   └── cache/              # 快取資料
│
├── 🎨 前端資源
│   ├── templates/          # HTML模板
│   │   ├── auth/           # 認證相關頁面
│   │   ├── member/         # 會員專區
│   │   ├── home.html       # 首頁
│   │   ├── stock.html      # 個股頁面
│   │   └── chatbot.html    # 智能問答
│   └── static/
│       ├── style.css       # 自定義樣式
│       └── chart_test.html # 圖表測試
│
└── 📊 資料和日誌
    ├── instance/           # SQLite資料庫
    ├── data/               # 知識庫資料
    └── logs/               # 系統日誌
```

## 🛠 技術架構

### 後端技術棧
- **Web框架**：Flask 2.3+ + Flask-Login + Flask-SQLAlchemy
- **資料庫**：SQLite + SQLAlchemy 2.0
- **資料來源**：Yahoo Finance API
- **AI/ML**：sentence-transformers + FAISS + OpenAI GPT

### 前端技術棧
- **UI框架**：Bootstrap 5
- **圖表庫**：Chart.js（計劃中）
- **前端邏輯**：原生 JavaScript
- **圖標**：Bootstrap Icons

### RAG系統架構
- **嵌入模型**：paraphrase-multilingual-MiniLM-L12-v2
- **向量資料庫**：FAISS
- **語言模型**：OpenAI GPT-3.5-turbo（可選）
- **知識來源**：財經新聞、投資知識、技術分析

## 🌐 功能頁面

| 路由 | 功能描述 | 權限需求 |
|------|----------|----------|
| `/` | 首頁 - 股票搜尋、大盤資訊 | 公開 |
| `/stock/<code>` | 個股詳細資訊頁面 | 公開 |
| `/chatbot` | RAG智能問答系統 | 公開 |
| `/auth/login` | 用戶登入 | 公開 |
| `/auth/register` | 用戶註冊 | 公開 |
| `/member/dashboard` | 會員控制台 | 會員 |
| `/member/watchlist` | 自選股管理 | 會員 |
| `/member/profile` | 個人資料設定 | 會員 |

## ⚙️ 進階配置

### RAG系統設定
```bash
# 完整安裝 RAG 系統
cd rag
python setup.py

# 配置 OpenAI API（可選但推薦）
python ../setup_openai.py
```

### 資料庫管理
```bash
python database/manage.py
# 1. 初始化資料庫        # 首次使用必須
# 2. 查看資料內容        # 檢視資料庫狀態
# 3. 備份資料庫         # 定期備份建議
# 4. 恢復資料庫         # 災難恢復
# 5. 統計資訊          # 系統使用統計
```

### OpenAI API 設定
編輯 `config/rag_config.json`：
```json
{
  "openai_api_key": "your-api-key-here",
  "openai_model": "gpt-3.5-turbo",
  "enable_openai": true,
  "enable_fallback": true,
  "max_tokens": 500,
  "temperature": 0.7
}
```

## 📦 依賴管理

### 核心依賴
```bash
# Web 框架
Flask>=2.3.0
Flask-SQLAlchemy>=3.0.0
Flask-Login>=0.6.0
Flask-WTF>=1.1.0

# 資料處理
requests>=2.28.0
pandas>=1.5.0
beautifulsoup4>=4.11.0
```

### RAG 系統依賴
```bash
# AI/ML 核心
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
scikit-learn>=1.0.0

# OpenAI 整合（可選）
openai>=1.0.0
```

### 安裝策略
```bash
# 基礎功能（不含AI）
pip install flask flask-sqlalchemy flask-login flask-wtf requests pandas

# 完整功能（含RAG）
pip install -r requirements.txt
```

## 🧪 測試和除錯

### 快速測試
```bash
# RAG 系統功能測試
python rag/tests/quick_test.py

# 資料庫完整性檢查
python database/manage.py  # 選項 5

# 股票API連線測試
python -c "from utils.twse import get_market_summary; print(get_market_summary())"
```

### 開發工具
```bash
# 資料庫瀏覽器
python db_viewer.py

# 日誌查看
tail -f logs/rag_system.log  # Linux/Mac
type logs\rag_system.log     # Windows
```

## 🎨 使用範例

### 股票查詢
```
輸入：2330    → 台積電完整資訊
輸入：0050    → 台灣50 ETF資訊
輸入：大盤     → 市場概況資料
```

### RAG智能問答
```
「台積電股價多少？」           → 即時股價 + 公司介紹
「什麼是技術分析？」          → 專業知識解答
「如何判斷股票的投資價值？」   → 投資策略指導
「今天大盤表現如何？」        → 市場分析報告
```

## ⚠️ 重要注意事項

### 系統需求
- **記憶體**：建議 1GB+ 可用記憶體（RAG模型約需 500MB）
- **儲存空間**：基礎安裝需要 2GB，完整安裝需要 3GB+
- **網路**：需要穩定網路連線以獲取即時股價資料

### 資料說明
- **股價資料**：來源 Yahoo Finance，有 5 分鐘快取延遲
- **RAG知識庫**：首次啟動需下載模型（約 500MB）
- **資料庫**：SQLite 檔案位於 `instance/stock_app.db`

### 效能優化
- 啟用快取機制減少API調用
- RAG模型使用本地嵌入以提升響應速度
- 資料庫連接池優化並發處理

## 📚 相關文檔

- 📖 [RAG系統詳細說明](rag/README.md)
- 🗄️ [資料庫管理指南](database/README.md)
- 🤖 [RAG使用說明](rag/docs/RAG_使用說明.md)
- 🚀 [RAG部署總結](rag/docs/RAG_成功部署總結.md)

## 🔮 未來規劃

- [ ] 技術圖表功能強化
- [ ] 更多技術指標支援
- [ ] 行動端 APP 開發
- [ ] 即時價格推送
- [ ] 更豐富的財經新聞整合
- [ ] 投資組合分析工具

## 🤝 貢獻指南

歡迎提交 Issues 和 Pull Requests！請確保：
- 代碼符合 PEP 8 標準
- 包含適當的測試
- 更新相關文檔

## 📄 授權條款

本專案採用 MIT 授權條款。

---

**⚡ 立即體驗您的智能財經系統！**

**🚨 免責聲明**：本系統提供的股價資訊僅供參考，不構成投資建議。投資有風險，請謹慎評估後做出決策。 
