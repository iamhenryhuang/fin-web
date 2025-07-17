# RAG系統整合到語言模型指南

## 概述

本指南將教您如何將RAG（Retrieval-Augmented Generation）系統整合到真實的語言模型中，擺脫手刻知識庫的限制。

## 系統架構

```
用戶查詢 → 嵌入模型 → 向量檢索 → 語言模型 → 生成回答
    ↓           ↓           ↓           ↓
 文本預處理    向量化      相似度搜索    上下文融合
```

## 快速開始

### 1. 安裝進階RAG系統

```bash
# 運行自動安裝腳本
python setup_advanced_rag.py
```

這個腳本會：
- 檢查Python版本（需要3.8+）
- 安裝必要依賴包
- 創建目錄結構
- 設置配置文件
- 初始化知識庫
- 測試系統功能

### 2. 配置API Keys

編輯 `config/rag_config.json`：

```json
{
  "openai_api_key": "your-openai-api-key-here",
  "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "openai_model": "gpt-3.5-turbo"
}
```

### 3. 使用增強版Chatbot

```python
from utils.enhanced_chatbot import EnhancedChatBot
import asyncio

# 初始化
chatbot = EnhancedChatBot()

# 異步查詢
async def test_query():
    result = await chatbot.process_message("什麼是股票投資？")
    print(result["answer"])

# 運行
asyncio.run(test_query())
```

## 核心功能

### 1. 多層次回退機制

系統具有智能回退機制：

1. **進階RAG + OpenAI GPT** - 最佳性能
2. **本地嵌入模型 + 模板生成** - 無需API key
3. **關鍵詞匹配 + 規則回答** - 最基本功能

### 2. 動態知識庫

```python
# 添加新知識
new_documents = [
    {
        "title": "ESG投資趨勢",
        "content": "ESG投資考慮環境、社會和治理因素...",
        "category": "投資趨勢",
        "source": "財經新聞"
    }
]

await chatbot.add_knowledge(new_documents)
```

### 3. 向量檢索

使用FAISS進行高效向量檢索：

```python
# 檢索相關文檔
docs = chatbot.enhanced_bot.rag_system.retrieve_documents(
    "技術分析是什麼？", 
    top_k=5
)

for doc in docs:
    print(f"相似度: {doc['similarity_score']:.3f}")
    print(f"標題: {doc['title']}")
```

## 進階配置

### 1. 選擇嵌入模型

```json
{
  "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
}
```

可選模型：
- `paraphrase-multilingual-MiniLM-L12-v2` - 多語言，支援中文
- `all-MiniLM-L6-v2` - 快速，主要英文
- `openai` - 使用OpenAI embeddings API

### 2. 調整檢索參數

```json
{
  "top_k_retrieve": 3,
  "confidence_threshold": 0.3,
  "temperature": 0.7,
  "max_tokens": 500
}
```

### 3. 自定義提示詞

在 `utils/advanced_rag.py` 中修改 `_openai_generate` 方法：

```python
prompt = f"""
你是專業的財經顧問。基於以下資訊回答問題：

上下文: {context}
問題: {query}

請用繁體中文回答，並提供具體建議：
"""
```

## 網路資料收集

### 1. 自動收集新聞

```python
from utils.advanced_rag import WebKnowledgeCollector

collector = WebKnowledgeCollector()
news_data = await collector.collect_stock_news("2330")

# 添加到知識庫
await chatbot.add_knowledge(news_data)
```

### 2. 定期更新知識庫

```python
import schedule
import time

def update_knowledge():
    # 收集最新財經資訊
    # 更新向量索引
    pass

# 每日更新
schedule.every().day.at("06:00").do(update_knowledge)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 性能優化

### 1. 向量資料庫優化

```python
# 使用GPU加速（如果可用）
"vector_db_type": "faiss-gpu"

# 建立索引時進行聚類
index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
```

### 2. 快取機制

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_hash):
    # 快取常見查詢結果
    pass
```

### 3. 批次處理

```python
# 批次生成嵌入向量
embeddings = model.encode(texts, batch_size=32)
```

## 監控與日誌

### 1. 系統狀態監控

```python
status = chatbot.get_system_status()
print(f"知識庫大小: {status['knowledge_base_size']}")
print(f"向量資料庫: {status['has_vector_db']}")
print(f"OpenAI可用: {status['has_openai']}")
```

### 2. 查詢分析

```python
# 分析查詢性能
result = await chatbot.process_message("查詢內容")
print(f"回應時間: {result['response_time']:.2f}秒")
print(f"信心度: {result['confidence']:.2f}")
print(f"檢索方法: {result['method']}")
```

### 3. 日誌配置

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/rag_system.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

## 故障排除

### 1. 依賴包問題

```bash
# 重新安裝sentence-transformers
pip install --force-reinstall sentence-transformers

# 使用CPU版本的FAISS
pip install faiss-cpu
```

### 2. 記憶體不足

```python
# 減少批次大小
"batch_size": 16

# 使用較小的模型
"embedding_model": "all-MiniLM-L6-v2"
```

### 3. API調用失敗

```python
# 設置重試機制
import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    stop=tenacity.stop_after_attempt(3)
)
async def call_openai_api(prompt):
    # API調用邏輯
    pass
```

## 擴展功能

### 1. 多模態支援

```python
# 添加圖片處理
from PIL import Image
import torch
from transformers import CLIPModel

# 圖文檢索
def image_text_search(image, text):
    # 實現圖文聯合檢索
    pass
```

### 2. 個性化推薦

```python
# 用戶偏好學習
class UserPreference:
    def __init__(self):
        self.user_interests = {}
    
    def update_preference(self, user_id, query, feedback):
        # 更新用戶偏好
        pass
```

### 3. 多語言支援

```python
# 語言檢測和翻譯
from googletrans import Translator

translator = Translator()

def auto_translate(text, target_lang='zh-tw'):
    return translator.translate(text, dest=target_lang).text
```

## 最佳實踐

### 1. 知識庫設計

- **結構化資料**：使用統一的文檔格式
- **語義標籤**：添加分類和標籤
- **時間戳記**：追蹤資訊更新時間
- **來源追蹤**：記錄資訊來源

### 2. 檢索策略

- **混合檢索**：結合語義和關鍵詞檢索
- **重排序**：使用交叉編碼器重新排序
- **多輪檢索**：支援對話上下文
- **負面過濾**：過濾不相關內容

### 3. 生成控制

- **溫度調節**：控制回答的創造性
- **長度限制**：避免過長回答
- **事實檢查**：驗證生成內容
- **安全過濾**：過濾不當內容

## 總結

通過這個進階RAG系統，您可以：

1. **擺脫手刻知識庫**：使用真實的向量資料庫和語言模型
2. **動態更新知識**：從網路收集最新資訊
3. **智能回退**：確保系統穩定性
4. **高性能檢索**：使用向量相似度搜索
5. **自然語言生成**：產生流暢的回答

這個系統為您的財經chatbot提供了專業級的RAG能力，讓用戶能夠獲得更準確、更及時的財經資訊和建議。 