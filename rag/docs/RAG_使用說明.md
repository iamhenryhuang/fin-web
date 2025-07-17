# RAG系統使用說明

## 概述

您的財經聊天機器人現在已經升級為RAG（Retrieval-Augmented Generation）系統，擁有更強大的知識查詢和回答能力。

## 新功能特色

### 🧠 知識查詢
- **財經術語解釋**：「什麼是本益比？」「ROE是什麼意思？」
- **投資策略說明**：「價值投資是什麼？」「如何分散投資風險？」
- **技術分析教學**：「移動平均線怎麼看？」「RSI指標如何使用？」
- **市場基礎知識**：「股票代碼怎麼分類？」「台股交易時間是什麼時候？」

### 💭 對話記憶
- 系統會記住對話上下文，提供更連貫的回答
- 支援多輪對話，可以進行深入討論

### 📚 來源追蹤
- 顯示回答的資料來源
- 提供相關文檔預覽
- 信心評分顯示回答的可信度

### 🔄 即時股價 + 知識結合
- 既能查詢即時股價，又能解釋相關概念
- 例如：「台積電股價多少？順便解釋一下半導體產業」

## 安裝步驟

### 1. 安裝依賴
```bash
pip install -r requirements_rag.txt
```

### 2. 初始化系統
```bash
python setup_rag.py
```

### 3. 啟動應用
```bash
python app.py
```

## 使用範例

### 基本股票查詢（原有功能）
- 「台積電今天收盤多少？」
- 「大盤怎麼樣？」
- 「2330漲跌幅如何？」

### 知識查詢（新功能）
- 「什麼是本益比？」
- 「價值投資策略是什麼？」
- 「如何看懂K線圖？」
- 「新手該如何開始投資？」

### 綜合查詢
- 「台積電的本益比高嗎？什麼是合理的本益比？」
- 「0050是什麼？適合新手投資嗎？」
- 「技術分析和基本面分析有什麼差別？」

## 系統架構

### 核心組件
1. **知識庫 (KnowledgeBase)**：儲存財經知識文檔
2. **向量存儲 (VectorStore)**：使用FAISS進行高效相似度搜索
3. **嵌入服務 (EmbeddingService)**：使用sentence-transformers生成文本嵌入
4. **檢索器 (Retriever)**：根據查詢檢索相關文檔
5. **回答生成器 (ResponseGenerator)**：基於檢索結果生成回答

### 資料流程
1. 用戶輸入問題
2. 系統判斷查詢類型（股價查詢 vs 知識查詢）
3. 如果是知識查詢：
   - 生成問題的嵌入向量
   - 在向量資料庫中搜索相似文檔
   - 基於檢索結果生成回答
4. 如果是股價查詢：
   - 使用原有的股價查詢邏輯
5. 返回結果並記錄對話歷史

## 知識庫內容

### 股票基礎知識
- 股票定義和概念
- 股票代碼系統
- 交易時間和規則
- 漲跌幅限制
- 成交量概念

### 財經術語
- 本益比 (P/E Ratio)
- 股價淨值比 (P/B Ratio)
- 股息殖利率
- 市值概念
- ROE (股東權益報酬率)

### 台股市場資訊
- 台積電公司介紹
- 鴻海公司介紹
- 台灣加權指數
- 元大台灣50 ETF
- 產業分類

### 投資策略
- 價值投資
- 成長投資
- 定期定額投資
- 資產配置

### 技術分析
- 移動平均線
- RSI指標
- 支撐與壓力
- K線圖

## 擴展功能

### 添加新知識
```python
from utils.knowledge_initializer import KnowledgeInitializer

initializer = KnowledgeInitializer()

# 添加新聞知識
news_data = [
    {
        'title': '新聞標題',
        'content': '新聞內容',
        'tags': ['標籤1', '標籤2'],
        'source': '新聞來源',
        'date': '2024-01-01'
    }
]
initializer.add_news_knowledge(news_data)

# 添加公司資料
company_data = [
    {
        'name': '公司名稱',
        'stock_code': '1234',
        'industry': '產業類別',
        'description': '公司簡介',
        'business': '主要業務',
        'financial_info': '財務狀況'
    }
]
initializer.add_company_knowledge(company_data)
```

### 自訂配置
```python
from utils.rag_system import initialize_rag_system

config = {
    'embedding': {
        'model_name': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        'device': 'cuda'  # 使用GPU加速
    },
    'retrieval': {
        'top_k': 10,  # 檢索更多相關文檔
        'similarity_threshold': 0.3  # 降低相似度門檻
    }
}

rag_system = initialize_rag_system(config)
```

## 故障排除

### 常見問題

1. **FAISS安裝失敗**
   - 解決方案：使用 `pip install faiss-cpu` 而非 `faiss-gpu`

2. **sentence-transformers模型下載緩慢**
   - 解決方案：使用國內鏡像或手動下載模型

3. **記憶體不足**
   - 解決方案：減少batch_size或使用較小的嵌入模型

4. **回答質量不佳**
   - 解決方案：增加更多高質量的知識文檔

### 性能優化

1. **使用GPU加速**
   ```bash
   pip install faiss-gpu
   ```

2. **使用更好的嵌入模型**
   ```python
   config['embedding']['model_name'] = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
   ```

3. **調整檢索參數**
   ```python
   config['retrieval']['top_k'] = 3  # 減少檢索數量提升速度
   ```

## 未來發展方向

1. **整合更多資料來源**
   - 即時新聞爬蟲
   - 公司年報解析
   - 社群媒體情感分析

2. **多模態支援**
   - 圖表分析
   - 語音問答
   - 視覺化回答

3. **個性化推薦**
   - 基於用戶投資偏好
   - 風險承受度評估
   - 投資組合建議

4. **進階分析功能**
   - 股票估值模型
   - 技術指標計算
   - 市場趨勢預測

## 支援與反饋

如果您在使用過程中遇到問題或有改進建議，請記錄詳細的錯誤信息和使用場景，以便我們持續改進系統。 