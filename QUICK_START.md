# 🚀 快速開始指南

## 系統概述

現代化的台股查詢系統，整合RAG智能問答功能，提供即時股價查詢、財經知識問答和會員管理。

## 📋 系統需求

- Python 3.7+（推薦 3.8+）
- Windows/Linux/macOS
- 至少 2GB 可用空間

## 🔧 快速安裝

### 1. 基礎安裝

```bash
# 1. 安裝基礎依賴
pip install -r requirements.txt

# 2. 初始化資料庫
python database/manage.py
# 選擇選項 1 (初始化資料庫)

# 3. 啟動應用
python app.py
```

### 2. RAG智能問答系統安裝

```bash
# 進入RAG目錄
cd rag

# 運行統一安裝腳本
python setup.py

# 選擇安裝模式：
# 1. 基礎安裝 - 核心功能
# 2. 進階安裝 - 完整向量搜索（推薦）
# 3. 開發者安裝 - 包含測試工具
```

## 🎯 功能體驗

### 股票查詢功能

訪問：`http://127.0.0.1:5000`

- 輸入股票代碼（如：2330、0050）
- 查看即時股價和大盤資訊
- 使用會員功能管理自選股

### RAG智能問答

訪問：`http://127.0.0.1:5000/chatbot`

#### 🧠 試試這些問題：

**財經知識：**
- 「什麼是本益比？」
- 「價值投資的核心原則是什麼？」
- 「如何分散投資風險？」

**技術分析：**
- 「移動平均線怎麼看？」
- 「RSI指標如何使用？」
- 「MACD指標的原理是什麼？」

**即時股價：**
- 「台積電今天收盤多少？」
- 「大盤怎麼樣？」
- 「2330漲跌幅如何？」

**複合查詢：**
- 「台積電股價多少？順便解釋一下半導體產業」
- 「0050今天表現如何？這是什麼ETF？」

## 📁 目錄結構

```
financial_web/
├── app.py              # 主應用程式
├── models.py           # 資料庫模型
├── forms.py            # 表單定義
├── README.md           # 主項目說明
├── QUICK_START.md      # 本快速指南
├── rag/                # RAG智能問答系統
│   ├── core/           # 核心RAG實現
│   ├── setup/          # 安裝腳本
│   ├── tests/          # 測試腳本
│   ├── docs/           # 詳細文檔
│   ├── setup.py        # 統一安裝腳本
│   └── README.md       # RAG系統說明
├── database/           # 資料庫管理系統
│   ├── models.py       # 資料庫模型
│   ├── manage.py       # 統一管理工具
│   ├── utils/          # 資料庫工具
│   └── README.md       # Database說明
├── utils/              # 工具函數
│   └── twse.py         # 台股資料接口
├── templates/          # HTML模板
├── static/             # 靜態資源
├── config/             # 配置文件
├── data/               # 資料目錄
└── cache/              # 快取目錄
```

## 🔧 進階配置

### OpenAI API設置（可選）

1. 編輯 `config/rag_config.json`
2. 添加您的OpenAI API Key：

```json
{
  "openai_api_key": "your-openai-api-key-here",
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
  "openai_model": "gpt-3.5-turbo"
}
```

### 自定義知識庫

```python
from rag.core.knowledge_initializer import KnowledgeInitializer

initializer = KnowledgeInitializer()
initializer.add_document(
    title="自定義財經知識",
    content="您的專業知識內容...",
    category="財經知識"
)
initializer.save_knowledge_base()
```

## 🧪 系統測試

```bash
# 快速功能測試
cd rag
python tests/quick_test.py

# 完整RAG系統測試
python tests/test_advanced_rag.py
```

## 🐛 常見問題

### Q: RAG系統無法導入？
```bash
# 確保在正確目錄
cd financial_web
python -c "from rag.core.simple_rag import SimpleRAGSystem; print('✅ 導入成功')"
```

### Q: Python版本檢查失敗？
確保使用Python 3.7+，之前的版本比較bug已修復。

### Q: 模型下載失敗？
檢查網路連接，sentence-transformers模型約471MB。

### Q: 股價查詢失敗？
檢查網路連接和Yahoo Finance API可用性。

## 📚 詳細文檔

- **RAG系統完整說明**：[`rag/README.md`](rag/README.md)
- **主項目說明**：[`README.md`](README.md)
- **RAG使用說明**：[`rag/docs/RAG_使用說明.md`](rag/docs/RAG_使用說明.md)
- **RAG整合指南**：[`rag/docs/RAG_整合指南.md`](rag/docs/RAG_整合指南.md)

## 🎉 開始使用

1. **基礎功能**：運行 `python app.py` 後訪問 `http://127.0.0.1:5000`
2. **RAG問答**：進入 `rag/` 目錄運行 `python setup.py` 安裝
3. **測試系統**：運行 `python rag/tests/quick_test.py` 驗證功能

**享受您的智能財經查詢系統！** 🚀📈🤖 