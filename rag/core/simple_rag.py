#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版RAG系統 - 不依賴外部包
"""

import json
import re
import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SimpleRAGSystem:
    """簡化版RAG系統"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.initialized = True
        logger.info("簡化版RAG系統初始化完成")
    
    def _initialize_knowledge_base(self) -> List[Dict[str, Any]]:
        """初始化知識庫"""
        return [
            {
                "id": "stock_basic_001",
                "title": "什麼是股票",
                "content": "股票是公司發行的有價證券，代表股東對公司的所有權份額。持有股票意味著擁有公司的一部分，可以享受公司盈利分配（股息）和資本增值的權利。股票可以在證券交易所買賣，價格會根據市場供需關係波動。",
                "category": "股票基礎",
                "tags": ["股票", "投資", "證券"],
                "keywords": ["股票", "公司", "股東", "所有權", "股息", "資本增值", "證券交易所", "買賣", "價格", "市場"]
            },
            {
                "id": "stock_basic_002",
                "title": "股票代碼系統",
                "content": "台灣股票代碼是4位數字，例如台積電是2330。代碼的第一位數字通常代表產業類別：1開頭是水泥、食品等傳統產業，2開頭是塑膠、紡織、電機、化學等，3開頭是鋼鐵、橡膠等，4開頭是機械、電器電纜等，5開頭是電子、資訊等高科技產業，6開頭是營建、運輸等，8開頭是金融保險業，9開頭是貿易百貨業。",
                "category": "股票基礎",
                "tags": ["股票代碼", "分類", "台股"],
                "keywords": ["股票代碼", "台灣", "4位數字", "台積電", "2330", "產業類別", "傳統產業", "高科技", "電子", "金融"]
            },
            {
                "id": "term_001",
                "title": "本益比 (P/E Ratio)",
                "content": "本益比是股價與每股盈餘的比值，計算公式為：本益比 = 股價 ÷ 每股盈餘(EPS)。本益比反映投資人願意為每元盈餘支付多少錢，是評估股票是否便宜的重要指標。一般來說，本益比越低表示股票相對便宜，但也要考慮公司的成長性和產業特性。",
                "category": "財經術語",
                "tags": ["本益比", "PE", "估值", "投資分析"],
                "keywords": ["本益比", "PE", "P/E", "股價", "每股盈餘", "EPS", "計算公式", "投資人", "評估", "便宜", "成長性"]
            },
            {
                "id": "term_002",
                "title": "股價淨值比 (P/B Ratio)",
                "content": "股價淨值比是股價與每股淨值的比值，計算公式為：股價淨值比 = 股價 ÷ 每股淨值。這個比率反映市場對公司資產的評價，比值越低表示股票相對便宜。通常用於評估資產密集型企業，如銀行、保險、營建等行業。",
                "category": "財經術語",
                "tags": ["股價淨值比", "PB", "淨值", "資產評價"],
                "keywords": ["股價淨值比", "PB", "P/B", "股價", "每股淨值", "比值", "市場", "資產", "評價", "銀行", "保險", "營建"]
            },
            {
                "id": "term_003",
                "title": "股息殖利率",
                "content": "股息殖利率是年度股息與股價的比值，計算公式為：股息殖利率 = 年度股息 ÷ 股價 × 100%。這個指標反映投資股票的現金收益率，類似銀行存款利率。高股息殖利率的股票通常受到追求穩定收益的投資人青睞。",
                "category": "財經術語",
                "tags": ["股息殖利率", "股息", "現金收益", "被動收入"],
                "keywords": ["股息殖利率", "年度股息", "股價", "現金收益率", "銀行存款", "利率", "高股息", "穩定收益", "投資人"]
            },
            {
                "id": "taiwan_001",
                "title": "台積電 (2330)",
                "content": "台積電是全球最大的晶圓代工廠，成立於1987年，總部位於新竹科學園區。公司主要業務為積體電路製造服務，客戶包括蘋果、NVIDIA、AMD等知名科技公司。台積電在先進製程技術方面領先全球，是台股市值最大的公司，也是台灣最重要的科技企業之一。",
                "category": "台股個股",
                "tags": ["台積電", "2330", "半導體", "晶圓代工"],
                "keywords": ["台積電", "2330", "晶圓代工", "1987", "新竹科學園區", "積體電路", "蘋果", "NVIDIA", "AMD", "先進製程", "台股", "市值", "科技企業"]
            },
            {
                "id": "taiwan_002",
                "title": "鴻海 (2317)",
                "content": "鴻海精密工業股份有限公司是全球最大的電子製造服務商，成立於1974年。公司主要從事電子產品代工製造，包括智慧型手機、電腦、遊戲機等。鴻海是蘋果iPhone的主要組裝廠商，在中國大陸設有多個生產基地。近年來積極轉型，投入電動車、半導體等新興產業。",
                "category": "台股個股",
                "tags": ["鴻海", "2317", "電子製造", "代工"],
                "keywords": ["鴻海", "2317", "電子製造", "1974", "代工製造", "智慧型手機", "電腦", "遊戲機", "蘋果", "iPhone", "中國大陸", "電動車", "半導體"]
            },
            {
                "id": "taiwan_003",
                "title": "元大台灣50 (0050)",
                "content": "元大台灣50 ETF追蹤台灣50指數，投資台灣市值最大的50家上市公司。這是台灣第一檔ETF，成立於2003年，管理費用低廉，適合長期投資。由於分散投資於台股龍頭企業，風險相對較低，是許多投資新手的首選標的。",
                "category": "台股ETF",
                "tags": ["0050", "ETF", "台灣50", "被動投資"],
                "keywords": ["元大台灣50", "0050", "ETF", "台灣50指數", "50家", "上市公司", "2003", "管理費用", "長期投資", "分散投資", "龍頭企業", "風險", "新手"]
            },
            {
                "id": "strategy_001",
                "title": "價值投資",
                "content": "價值投資是尋找被市場低估的股票進行長期投資的策略。投資者通過分析公司的基本面，如財務狀況、盈利能力、成長前景等，找出內在價值高於市場價格的股票。著名的價值投資者包括巴菲特、葛拉漢等。關鍵指標包括本益比、股價淨值比、股息殖利率等。",
                "category": "投資策略",
                "tags": ["價值投資", "巴菲特", "基本面分析", "長期投資"],
                "keywords": ["價值投資", "市場低估", "長期投資", "基本面", "財務狀況", "盈利能力", "成長前景", "內在價值", "市場價格", "巴菲特", "葛拉漢", "本益比", "股價淨值比", "股息殖利率"]
            },
            {
                "id": "strategy_002",
                "title": "定期定額投資",
                "content": "定期定額投資是每月固定投資一定金額購買股票或基金的策略。這種方式可以分散投資時點，降低市場波動的影響，適合長期累積財富。當股價下跌時買到更多股數，股價上漲時買到較少股數，長期下來可以平均成本。特別適合投資ETF或績優股。",
                "category": "投資策略",
                "tags": ["定期定額", "平均成本", "長期投資", "ETF"],
                "keywords": ["定期定額", "每月", "固定投資", "股票", "基金", "分散投資", "市場波動", "長期累積", "財富", "股價下跌", "股價上漲", "平均成本", "ETF", "績優股"]
            },
            {
                "id": "technical_001",
                "title": "移動平均線",
                "content": "移動平均線是技術分析中最常用的指標之一，計算一定期間內股價的平均值。常用的有5日、10日、20日、60日移動平均線。當股價在移動平均線之上時，通常表示上升趨勢；反之則表示下降趨勢。黃金交叉（短期均線向上突破長期均線）被視為買進訊號，死亡交叉則為賣出訊號。",
                "category": "技術分析",
                "tags": ["移動平均線", "MA", "黃金交叉", "死亡交叉"],
                "keywords": ["移動平均線", "技術分析", "股價", "平均值", "5日", "10日", "20日", "60日", "上升趨勢", "下降趨勢", "黃金交叉", "死亡交叉", "買進訊號", "賣出訊號"]
            },
            {
                "id": "technical_002",
                "title": "RSI相對強弱指標",
                "content": "RSI是衡量股價漲跌動能的震盪指標，數值介於0-100之間。當RSI超過70時，表示股票可能超買，有回檔壓力；當RSI低於30時，表示股票可能超賣，有反彈機會。RSI也可以用來判斷背離現象，當股價創新高但RSI未創新高時，可能是賣出訊號。",
                "category": "技術分析",
                "tags": ["RSI", "相對強弱指標", "超買", "超賣"],
                "keywords": ["RSI", "相對強弱指標", "股價", "漲跌動能", "震盪指標", "0-100", "超買", "70", "回檔壓力", "超賣", "30", "反彈機會", "背離現象", "創新高", "賣出訊號"]
            }
        ]
    
    def _calculate_similarity(self, query: str, document: Dict[str, Any]) -> float:
        """計算查詢與文檔的相似度"""
        query_lower = query.lower()
        query_words = [word for word in query_lower.split() if len(word) > 1]
        
        if not query_words:
            return 0.0
        
        # 檢查關鍵詞匹配
        keyword_matches = 0
        for keyword in document.get('keywords', []):
            if keyword.lower() in query_lower:
                keyword_matches += 1
        
        # 檢查標題匹配
        title_matches = 0
        title_lower = document['title'].lower()
        for word in query_words:
            if word in title_lower:
                title_matches += 1
        
        # 檢查內容匹配
        content_matches = 0
        content_lower = document['content'].lower()
        for word in query_words:
            if word in content_lower:
                content_matches += 1
        
        # 計算相似度分數
        total_matches = keyword_matches * 3 + title_matches * 2 + content_matches * 1
        
        # 基於匹配數量計算相似度
        if total_matches == 0:
            return 0.0
        
        # 正規化分數
        max_score = len(query_words) * 6  # 假設每個詞都能在關鍵詞、標題、內容中匹配
        similarity = min(total_matches / max_score, 1.0)
        
        # 如果標題直接包含查詢的主要概念，給予額外加分
        if any(word in title_lower for word in ['本益比', '股價淨值比', '股息殖利率', '台積電', '鴻海', '價值投資', '定期定額', '移動平均線', 'rsi']):
            for word in query_words:
                if word in title_lower:
                    similarity += 0.2
        
        return min(similarity, 1.0)
    
    def query(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """處理查詢並返回回答"""
        try:
            # 計算每個文檔的相似度
            scored_docs = []
            for doc in self.knowledge_base:
                similarity = self._calculate_similarity(question, doc)
                if similarity > 0.1:  # 只保留相似度大於0.1的文檔
                    scored_docs.append((doc, similarity))
            
            # 按相似度排序
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            if not scored_docs:
                return {
                    'answer': "抱歉，我沒有找到相關的資訊來回答您的問題。",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # 使用最相關的文檔生成回答
            best_doc, best_score = scored_docs[0]
            
            # 生成回答
            answer = f"根據我的知識庫，{best_doc['content']}"
            
            # 如果有多個相關文檔，可以補充資訊
            if len(scored_docs) > 1 and scored_docs[1][1] > 0.3:
                second_doc = scored_docs[1][0]
                if second_doc['category'] != best_doc['category']:
                    answer += f"\n\n另外，{second_doc['content']}"
            
            # 準備來源資訊
            sources = []
            for doc, score in scored_docs[:3]:
                sources.append({
                    'title': doc['title'],
                    'content_preview': doc['content'][:100] + '...' if len(doc['content']) > 100 else doc['content'],
                    'similarity': score,
                    'category': doc['category']
                })
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': best_score,
                'retrieved_docs': [{'document': doc, 'similarity_score': score} for doc, score in scored_docs[:5]]
            }
            
        except Exception as e:
            logger.error(f"查詢處理失敗: {e}")
            return {
                'answer': f"抱歉，處理您的問題時發生錯誤：{str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def add_knowledge(self, documents: List[Dict[str, Any]]):
        """添加知識到系統中"""
        for doc in documents:
            # 自動生成關鍵詞
            if 'keywords' not in doc:
                doc['keywords'] = self._extract_keywords(doc.get('content', ''))
            self.knowledge_base.append(doc)
        
        logger.info(f"成功添加 {len(documents)} 個文檔到知識庫")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """從文本中提取關鍵詞"""
        # 簡單的關鍵詞提取
        words = re.findall(r'\b\w+\b', text)
        # 過濾掉常見的停用詞
        stop_words = {'的', '是', '在', '有', '和', '與', '或', '但', '而', '等', '可以', '能夠', '通常', '一般', '主要', '重要', '包括'}
        keywords = [word for word in words if len(word) > 1 and word not in stop_words]
        return list(set(keywords))  # 去重

# 全域簡化RAG系統實例
simple_rag_system = None

def get_simple_rag_system() -> SimpleRAGSystem:
    """獲取全域簡化RAG系統實例"""
    global simple_rag_system
    if simple_rag_system is None:
        simple_rag_system = SimpleRAGSystem()
    return simple_rag_system 