# 🤖 RAG (Retrieval-Augmented Generation) 智能問答系統

一個完整的RAG系統實現，專為財經股票資料查詢和智能對話而設計。支援即時股價查詢、財經知識問答、自然語言理解，並提供多種RAG實現方式。

## 🚀 系統特色

### 💡 **智能問答能力**
- **財經知識庫**：內建12個專業財經文檔
- **即時股價查詢**：結合台股即時資料
- **語義理解**：支援中文自然語言查詢
- **上下文記憶**：多輪對話連貫性
- **來源追蹤**：顯示回答的資料來源和信心度

### 🔧 **多重RAG實現**
- **進階RAG系統** (`advanced_rag.py`)：完整向量搜索+語言模型
- **輕量級RAG** (`lightweight_rag.py`)：優化的高效實現
- **簡單RAG** (`simple_rag.py`)：基礎實現，易於理解
- **通用RAG系統** (`rag_system.py`)：統一接口

### 🛡️ **智能回退機制**
1. **第一層**：OpenAI GPT + 向量語義搜索（最佳效果）
2. **第二層**：本地模型 + 模板生成（離線可用）
3. **第三層**：關鍵詞匹配 + 規則回答（後備機制）

## 📁 目錄結構

```
rag/
├── core/                    # 核心RAG系統實現
│   ├── advanced_rag.py     # 進階RAG系統
│   ├── lightweight_rag.py  # 輕量級RAG
│   ├── simple_rag.py       # 簡單RAG實現
│   ├── rag_system.py       # 通用RAG系統
│   ├── knowledge_initializer.py  # 知識庫初始化
│   ├── chatbot.py          # 基礎聊天機器人
│   └── enhanced_chatbot.py # 增強聊天機器人
├── setup/                   # 安裝和設置腳本
│   ├── setup_advanced_rag.py  # 進階RAG安裝腳本
│   ├── setup_rag.py        # 基礎RAG安裝腳本
│   └── requirements_rag.txt # 依賴需求檔案
├── tests/                   # 測試腳本
│   ├── test_advanced_rag.py    # 進階RAG測試
│   ├── test_lightweight_rag.py # 輕量級RAG測試
│   ├── test_rag_system.py      # RAG系統測試
│   ├── test_simple_demo.py     # 簡單演示
│   └── quick_test.py        # 快速測試
└── README.md               # 本文檔
```

## 🚀 快速開始

### 1. 系統需求

- Python 3.7+（推薦 3.8+）
- Windows/Linux/macOS
- 至少 2GB 可用空間（用於模型下載）

### 2. 安裝進階RAG系統

```bash
# 進入RAG目錄
cd rag

# 運行自動安裝腳本
python setup/setup_advanced_rag.py
```

安裝腳本會自動：
- ✅ 檢查Python版本
- ✅ 安裝必要依賴包
- ✅ 下載多語言向量模型（471MB）
- ✅ 創建目錄結構
- ✅ 設置配置文件
- ✅ 初始化知識庫
- ✅ 測試系統功能

### 3. 配置API Keys（可選）

編輯 `config/rag_config.json`：

```json
{
  "openai_api_key": "your-openai-api-key-here",
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
  "openai_model": "gpt-3.5-turbo",
  "max_context_length": 4000,
  "similarity_threshold": 0.7
}
```

### 4. 快速測試

```bash
# 運行快速測試
python tests/quick_test.py

# 運行完整測試
python tests/test_advanced_rag.py
```

## 💻 使用方法

### 基本使用

```python
from rag.core.enhanced_chatbot import EnhancedChatBot

# 初始化聊天機器人
chatbot = EnhancedChatBot()

# 財經知識查詢
response = chatbot.query("什麼是技術分析？")
print(response)

# 即時股價查詢
response = chatbot.query("台積電今天收盤多少？")
print(response)

# 複合查詢
response = chatbot.query("台積電股價多少？順便解釋一下半導體產業")
print(response)
```

### 進階使用

```python
from rag.core.advanced_rag import AdvancedRAGSystem
import asyncio

async def advanced_demo():
    # 初始化進階RAG系統
    rag = AdvancedRAGSystem()
    await rag.initialize()
    
    # 查詢並獲取詳細資訊
    result = await rag.query(
        "價值投資的核心原則是什麼？", 
        include_sources=True,
        min_confidence=0.7
    )
    
    print(f"回答: {result['answer']}")
    print(f"信心度: {result['confidence']}")
    print(f"來源: {result['sources']}")

# 運行
asyncio.run(advanced_demo())
```

## 🧠 核心功能介紹

### 1. 智能財經問答

支援的查詢類型：

#### 📈 **財經知識**
- 「什麼是本益比？」
- 「ROE是什麼意思？」
- 「價值投資是什麼？」
- 「如何分散投資風險？」

#### 📊 **技術分析**
- 「移動平均線怎麼看？」
- 「RSI指標如何使用？」
- 「MACD指標的原理是什麼？」

#### 💰 **即時股價**
- 「台積電今天收盤多少？」
- 「大盤怎麼樣？」
- 「2330漲跌幅如何？」

#### 📚 **市場基礎**
- 「股票代碼怎麼分類？」
- 「台股交易時間是什麼時候？」
- 「什麼是除權除息？」

### 2. 對話記憶系統

```python
# 支援多輪對話
chatbot.query("什麼是價值投資？")
# 回答：價值投資是一種投資策略...

chatbot.query("這個策略的風險是什麼？")
# 系統記住上下文，知道"這個策略"指的是價值投資
```

### 3. 來源追蹤與信心度

```python
result = await rag.query("什麼是技術分析？", include_sources=True)

# 結果包含：
{
    "answer": "技術分析是通過研究股價圖表...",
    "confidence": 0.89,
    "sources": [
        {"document": "技術分析基礎", "score": 0.92},
        {"document": "投資策略指南", "score": 0.78}
    ]
}
```

## 🔧 系統架構

### RAG處理流程

```
用戶查詢 → 文本預處理 → 向量化 → 語義搜索 → 上下文融合 → 語言模型 → 生成回答
    ↓           ↓          ↓        ↓         ↓          ↓
 意圖識別    嵌入模型    向量檢索   相關文檔    提示工程    回答生成
```

### 技術棧

- **向量模型**：sentence-transformers（多語言支援）
- **向量資料庫**：FAISS（高效相似度搜索）
- **語言模型**：OpenAI GPT（可選）+ 本地後備
- **知識庫**：JSON格式，支援動態更新
- **Web框架**：Flask（整合到主應用）

## 📦 依賴包

核心依賴：
```
sentence-transformers>=2.2.0  # 向量嵌入模型
faiss-cpu>=1.7.0             # 向量搜索引擎
scikit-learn>=1.0.0          # 機器學習工具
pandas>=1.5.0                # 資料處理
requests>=2.28.0             # HTTP請求
beautifulsoup4>=4.11.0       # 網頁解析
openai>=1.0.0                # OpenAI API（可選）
```

完整依賴列表請參考 `setup/requirements_rag.txt`。

## 🧪 測試與驗證

### 運行測試套件

```bash
# 快速功能測試
python tests/quick_test.py

# 完整系統測試
python tests/test_advanced_rag.py

# 輕量級RAG測試
python tests/test_lightweight_rag.py

# 簡單演示
python tests/test_simple_demo.py
```

### 測試結果範例

```
🧪 測試系統功能...
✅ 模型載入成功
✅ 知識庫初始化成功
✅ 向量搜索功能正常
✅ 語義理解準確率: 89%
✅ 回答生成品質: 優秀
📊 演示結果: 2/2 成功
🎉 系統基本功能正常！
```

## 🔨 進階配置

### 自定義知識庫

```python
from rag.core.knowledge_initializer import KnowledgeInitializer

# 添加自定義知識
initializer = KnowledgeInitializer()
initializer.add_document(
    title="自定義財經知識",
    content="您的專業知識內容...",
    category="財經知識"
)
initializer.save_knowledge_base()
```

### 調整模型參數

```json
{
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
  "max_context_length": 4000,
  "similarity_threshold": 0.7,
  "max_results": 5,
  "temperature": 0.7
}
```

## 🐛 常見問題

### Q: Python版本檢查失敗？
A: 確保使用Python 3.7+。如果仍有問題，請檢查版本比較邏輯。

### Q: 模型下載失敗？
A: 檢查網路連接，模型檔案約471MB。可以使用VPN或更換下載源。

### Q: OpenAI API調用失敗？
A: 系統會自動回退到本地模型，不影響基本功能。

### Q: 回答品質不理想？
A: 可以調整 `similarity_threshold` 提高相關性，或添加更多知識庫內容。

## 🔄 版本更新

### v1.0.0 (當前版本)
- ✅ 完整RAG系統實現
- ✅ 多種RAG變體支援
- ✅ 智能回退機制
- ✅ 中文語義理解
- ✅ 財經知識庫整合

## 🤝 參與貢獻

歡迎提交Issue和Pull Request來改進系統！

## 📄 授權

本專案採用MIT授權條款。

---

**🎉 RAG系統部署成功！**

您現在擁有一個完整的智能問答系統，能夠：
- 📚 回答財經專業問題
- 📈 查詢即時股票資料
- 🧠 理解自然語言
- 💬 進行多輪對話
- 🔍 追蹤資料來源

立即開始使用：`python tests/quick_test.py` 🚀 