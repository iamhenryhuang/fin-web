#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知識庫初始化器
用於填充股票和財經相關的基礎知識
"""

import json
import requests
from datetime import datetime
from typing import List, Dict, Any
import logging
from .rag_system import get_rag_system

logger = logging.getLogger(__name__)

class KnowledgeInitializer:
    """知識庫初始化器"""
    
    def __init__(self):
        self.rag_system = get_rag_system()
        
    def initialize_basic_knowledge(self):
        """初始化基礎知識"""
        try:
            # 股票基礎知識
            stock_basics = self._get_stock_basics()
            
            # 財經術語
            financial_terms = self._get_financial_terms()
            
            # 台股市場資訊
            taiwan_stock_info = self._get_taiwan_stock_info()
            
            # 投資策略
            investment_strategies = self._get_investment_strategies()
            
            # 技術分析
            technical_analysis = self._get_technical_analysis()
            
            # 合併所有知識
            all_knowledge = (stock_basics + financial_terms + taiwan_stock_info + 
                           investment_strategies + technical_analysis)
            
            # 添加到RAG系統
            self.rag_system.add_knowledge(all_knowledge)
            
            logger.info(f"成功初始化 {len(all_knowledge)} 條基礎知識")
            
        except Exception as e:
            logger.error(f"初始化基礎知識失敗: {e}")
            raise
    
    def _get_stock_basics(self) -> List[Dict[str, Any]]:
        """獲取股票基礎知識"""
        return [
            {
                "id": "stock_basic_001",
                "title": "什麼是股票",
                "content": "股票是公司發行的有價證券，代表股東對公司的所有權份額。持有股票意味著擁有公司的一部分，可以享受公司盈利分配（股息）和資本增值的權利。股票可以在證券交易所買賣，價格會根據市場供需關係波動。",
                "category": "股票基礎",
                "tags": ["股票", "投資", "證券"],
                "source": "財經教育"
            },
            {
                "id": "stock_basic_002",
                "title": "股票代碼系統",
                "content": "台灣股票代碼是4位數字，例如台積電是2330。代碼的第一位數字通常代表產業類別：1開頭是水泥、食品等傳統產業，2開頭是塑膠、紡織、電機、化學等，3開頭是鋼鐵、橡膠等，4開頭是機械、電器電纜等，5開頭是電子、資訊等高科技產業，6開頭是營建、運輸等，8開頭是金融保險業，9開頭是貿易百貨業。",
                "category": "股票基礎",
                "tags": ["股票代碼", "分類", "台股"],
                "source": "證交所"
            },
            {
                "id": "stock_basic_003",
                "title": "股票交易時間",
                "content": "台灣股市交易時間為週一至週五上午9:00-13:30，中午12:00-13:00為休息時間。盤前交易時間為8:30-9:00，盤後交易時間為13:30-14:30。國定假日不交易。投資人可以在交易時間內透過證券商進行買賣。",
                "category": "股票基礎",
                "tags": ["交易時間", "台股", "證券交易"],
                "source": "證交所"
            },
            {
                "id": "stock_basic_004",
                "title": "股票漲跌幅限制",
                "content": "台灣股票每日漲跌幅限制為10%，即股價最高只能上漲10%，最低只能下跌10%。這個限制是為了防止股價過度波動，保護投資人權益。當股票達到漲停或跌停時，仍可以在該價位進行交易。",
                "category": "股票基礎",
                "tags": ["漲跌幅", "漲停", "跌停"],
                "source": "證交所"
            },
            {
                "id": "stock_basic_005",
                "title": "股票成交量",
                "content": "成交量是指在一定時間內股票交易的股數總和，通常以「張」為單位（1張=1000股）。成交量大表示市場活躍，投資人關注度高；成交量小則表示市場清淡。成交量常與股價走勢結合分析，是技術分析的重要指標。",
                "category": "股票基礎",
                "tags": ["成交量", "技術分析", "市場活躍度"],
                "source": "財經教育"
            }
        ]
    
    def _get_financial_terms(self) -> List[Dict[str, Any]]:
        """獲取財經術語"""
        return [
            {
                "id": "term_001",
                "title": "本益比 (P/E Ratio)",
                "content": "本益比是股價與每股盈餘的比值，計算公式為：本益比 = 股價 ÷ 每股盈餘(EPS)。本益比反映投資人願意為每元盈餘支付多少錢，是評估股票是否便宜的重要指標。一般來說，本益比越低表示股票相對便宜，但也要考慮公司的成長性和產業特性。",
                "category": "財經術語",
                "tags": ["本益比", "PE", "估值", "投資分析"],
                "source": "財經教育"
            },
            {
                "id": "term_002",
                "title": "股價淨值比 (P/B Ratio)",
                "content": "股價淨值比是股價與每股淨值的比值，計算公式為：股價淨值比 = 股價 ÷ 每股淨值。這個比率反映市場對公司資產的評價，比值越低表示股票相對便宜。通常用於評估資產密集型企業，如銀行、保險、營建等行業。",
                "category": "財經術語",
                "tags": ["股價淨值比", "PB", "淨值", "資產評價"],
                "source": "財經教育"
            },
            {
                "id": "term_003",
                "title": "股息殖利率",
                "content": "股息殖利率是年度股息與股價的比值，計算公式為：股息殖利率 = 年度股息 ÷ 股價 × 100%。這個指標反映投資股票的現金收益率，類似銀行存款利率。高股息殖利率的股票通常受到追求穩定收益的投資人青睞。",
                "category": "財經術語",
                "tags": ["股息殖利率", "股息", "現金收益", "被動收入"],
                "source": "財經教育"
            },
            {
                "id": "term_004",
                "title": "市值",
                "content": "市值是公司所有流通在外股票的總價值，計算公式為：市值 = 股價 × 流通股數。市值反映市場對公司整體價值的評估。根據市值大小，通常將公司分為大型股（市值超過500億）、中型股（市值100-500億）、小型股（市值100億以下）。",
                "category": "財經術語",
                "tags": ["市值", "大型股", "中型股", "小型股"],
                "source": "財經教育"
            },
            {
                "id": "term_005",
                "title": "ROE (股東權益報酬率)",
                "content": "ROE是衡量公司運用股東資金獲利能力的指標，計算公式為：ROE = 淨利潤 ÷ 股東權益 × 100%。ROE越高表示公司使用股東資金的效率越好，通常ROE超過15%被認為是優質公司。巴菲特特別重視這個指標來選股。",
                "category": "財經術語",
                "tags": ["ROE", "股東權益報酬率", "獲利能力", "價值投資"],
                "source": "財經教育"
            }
        ]
    
    def _get_taiwan_stock_info(self) -> List[Dict[str, Any]]:
        """獲取台股市場資訊"""
        return [
            {
                "id": "taiwan_001",
                "title": "台積電 (2330)",
                "content": "台積電是全球最大的晶圓代工廠，成立於1987年，總部位於新竹科學園區。公司主要業務為積體電路製造服務，客戶包括蘋果、NVIDIA、AMD等知名科技公司。台積電在先進製程技術方面領先全球，是台股市值最大的公司，也是台灣最重要的科技企業之一。",
                "category": "台股個股",
                "tags": ["台積電", "2330", "半導體", "晶圓代工"],
                "source": "公司資料"
            },
            {
                "id": "taiwan_002",
                "title": "鴻海 (2317)",
                "content": "鴻海精密工業股份有限公司是全球最大的電子製造服務商，成立於1974年。公司主要從事電子產品代工製造，包括智慧型手機、電腦、遊戲機等。鴻海是蘋果iPhone的主要組裝廠商，在中國大陸設有多個生產基地。近年來積極轉型，投入電動車、半導體等新興產業。",
                "category": "台股個股",
                "tags": ["鴻海", "2317", "電子製造", "代工"],
                "source": "公司資料"
            },
            {
                "id": "taiwan_003",
                "title": "台灣加權指數",
                "content": "台灣加權指數是台灣股市的主要指標，由台灣證券交易所編製，以1966年為基期（基期指數為100）。指數涵蓋在台灣證券交易所上市的所有股票，採用市值加權方式計算。加權指數反映整體股市的漲跌情況，是觀察台股表現的重要指標。",
                "category": "台股市場",
                "tags": ["加權指數", "台股", "市場指標"],
                "source": "證交所"
            },
            {
                "id": "taiwan_004",
                "title": "元大台灣50 (0050)",
                "content": "元大台灣50 ETF追蹤台灣50指數，投資台灣市值最大的50家上市公司。這是台灣第一檔ETF，成立於2003年，管理費用低廉，適合長期投資。由於分散投資於台股龍頭企業，風險相對較低，是許多投資新手的首選標的。",
                "category": "台股ETF",
                "tags": ["0050", "ETF", "台灣50", "被動投資"],
                "source": "基金資料"
            },
            {
                "id": "taiwan_005",
                "title": "台股產業分類",
                "content": "台股主要產業包括：電子科技業（半導體、電腦、通訊等）、金融業（銀行、保險、證券）、傳統製造業（鋼鐵、塑膠、紡織）、生技醫療業、營建業、運輸業等。其中電子科技業是台股的重要支柱，佔整體市值比重最高，台積電、鴻海等都屬於此類。",
                "category": "台股市場",
                "tags": ["產業分類", "電子業", "金融業", "製造業"],
                "source": "市場分析"
            }
        ]
    
    def _get_investment_strategies(self) -> List[Dict[str, Any]]:
        """獲取投資策略"""
        return [
            {
                "id": "strategy_001",
                "title": "價值投資",
                "content": "價值投資是尋找被市場低估的股票進行長期投資的策略。投資者通過分析公司的基本面，如財務狀況、盈利能力、成長前景等，找出內在價值高於市場價格的股票。著名的價值投資者包括巴菲特、葛拉漢等。關鍵指標包括本益比、股價淨值比、股息殖利率等。",
                "category": "投資策略",
                "tags": ["價值投資", "巴菲特", "基本面分析", "長期投資"],
                "source": "投資教育"
            },
            {
                "id": "strategy_002",
                "title": "成長投資",
                "content": "成長投資專注於投資具有高成長潛力的公司，即使目前股價看起來較高也願意買入。這類公司通常營收和獲利成長快速，在新興產業或具有創新技術。投資者看重的是未來的成長性而非當前的估值。科技股、生技股常是成長投資的標的。",
                "category": "投資策略",
                "tags": ["成長投資", "高成長", "科技股", "創新"],
                "source": "投資教育"
            },
            {
                "id": "strategy_003",
                "title": "定期定額投資",
                "content": "定期定額投資是每月固定投資一定金額購買股票或基金的策略。這種方式可以分散投資時點，降低市場波動的影響，適合長期累積財富。當股價下跌時買到更多股數，股價上漲時買到較少股數，長期下來可以平均成本。特別適合投資ETF或績優股。",
                "category": "投資策略",
                "tags": ["定期定額", "平均成本", "長期投資", "ETF"],
                "source": "投資教育"
            },
            {
                "id": "strategy_004",
                "title": "資產配置",
                "content": "資產配置是將投資資金分散到不同類型的資產上，如股票、債券、現金等，以降低整體投資風險。常見的配置原則包括「年齡配置法」（股票比重 = 100 - 年齡）、「核心衛星策略」（核心資產配置ETF，衛星資產配置個股）等。適當的資產配置可以在風險和報酬間取得平衡。",
                "category": "投資策略",
                "tags": ["資產配置", "風險管理", "分散投資", "平衡"],
                "source": "投資教育"
            }
        ]
    
    def _get_technical_analysis(self) -> List[Dict[str, Any]]:
        """獲取技術分析知識"""
        return [
            {
                "id": "technical_001",
                "title": "移動平均線",
                "content": "移動平均線是技術分析中最常用的指標之一，計算一定期間內股價的平均值。常用的有5日、10日、20日、60日移動平均線。當股價在移動平均線之上時，通常表示上升趨勢；反之則表示下降趨勢。黃金交叉（短期均線向上突破長期均線）被視為買進訊號，死亡交叉則為賣出訊號。",
                "category": "技術分析",
                "tags": ["移動平均線", "MA", "黃金交叉", "死亡交叉"],
                "source": "技術分析"
            },
            {
                "id": "technical_002",
                "title": "相對強弱指標 (RSI)",
                "content": "RSI是衡量股價漲跌動能的震盪指標，數值介於0-100之間。當RSI超過70時，表示股票可能超買，有回檔壓力；當RSI低於30時，表示股票可能超賣，有反彈機會。RSI也可以用來判斷背離現象，當股價創新高但RSI未創新高時，可能是賣出訊號。",
                "category": "技術分析",
                "tags": ["RSI", "相對強弱指標", "超買", "超賣"],
                "source": "技術分析"
            },
            {
                "id": "technical_003",
                "title": "支撐與壓力",
                "content": "支撐是股價下跌時遇到買盤支撐的價位，壓力是股價上漲時遇到賣壓的價位。支撐和壓力可以是整數關卡、前期高低點、移動平均線等。當股價突破壓力線時，原本的壓力可能轉為支撐；當股價跌破支撐線時，原本的支撐可能轉為壓力。",
                "category": "技術分析",
                "tags": ["支撐", "壓力", "突破", "跌破"],
                "source": "技術分析"
            },
            {
                "id": "technical_004",
                "title": "K線圖",
                "content": "K線圖是顯示股價走勢的圖表，每根K線包含開盤價、收盤價、最高價、最低價四個價格。紅K線表示收盤價高於開盤價（上漲），黑K線表示收盤價低於開盤價（下跌）。K線的實體和影線長短反映買賣力道，是技術分析的基礎工具。",
                "category": "技術分析",
                "tags": ["K線圖", "蠟燭圖", "開高低收", "買賣力道"],
                "source": "技術分析"
            }
        ]
    
    def add_news_knowledge(self, news_data: List[Dict[str, Any]]):
        """添加新聞知識"""
        try:
            formatted_news = []
            for news in news_data:
                formatted_news.append({
                    "id": f"news_{news.get('id', len(formatted_news))}",
                    "title": news.get('title', ''),
                    "content": news.get('content', ''),
                    "category": "財經新聞",
                    "tags": news.get('tags', []),
                    "source": news.get('source', '新聞'),
                    "publish_date": news.get('date', datetime.now().isoformat())
                })
            
            self.rag_system.add_knowledge(formatted_news)
            logger.info(f"成功添加 {len(formatted_news)} 條新聞知識")
            
        except Exception as e:
            logger.error(f"添加新聞知識失敗: {e}")
    
    def add_company_knowledge(self, company_data: List[Dict[str, Any]]):
        """添加公司資料知識"""
        try:
            formatted_companies = []
            for company in company_data:
                formatted_companies.append({
                    "id": f"company_{company.get('stock_code', len(formatted_companies))}",
                    "title": f"{company.get('name', '')} ({company.get('stock_code', '')})",
                    "content": f"公司名稱：{company.get('name', '')}\n"
                              f"股票代碼：{company.get('stock_code', '')}\n"
                              f"產業類別：{company.get('industry', '')}\n"
                              f"公司簡介：{company.get('description', '')}\n"
                              f"主要業務：{company.get('business', '')}\n"
                              f"財務狀況：{company.get('financial_info', '')}",
                    "category": "公司資料",
                    "tags": [company.get('stock_code', ''), company.get('industry', ''), "公司資料"],
                    "source": "公司年報"
                })
            
            self.rag_system.add_knowledge(formatted_companies)
            logger.info(f"成功添加 {len(formatted_companies)} 條公司知識")
            
        except Exception as e:
            logger.error(f"添加公司知識失敗: {e}")


def initialize_knowledge_base():
    """初始化知識庫的主函數"""
    try:
        initializer = KnowledgeInitializer()
        initializer.initialize_basic_knowledge()
        logger.info("知識庫初始化完成")
        return True
    except Exception as e:
        logger.error(f"知識庫初始化失敗: {e}")
        return False

if __name__ == "__main__":
    # 直接運行此腳本時初始化知識庫
    initialize_knowledge_base() 