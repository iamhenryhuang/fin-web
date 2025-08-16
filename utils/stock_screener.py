import requests
import json
import os
import time
import random
from datetime import datetime, timedelta
from utils.twse import get_stock_basic_info, get_stock_chart_data, HEADERS, CONFIG
try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None

class StockScreener:
    """股票選股器 - 基於技術指標進行選股分析"""
    
    def __init__(self):
        self.cache_dir = 'cache'
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 台股常見股票池（優化版 - 更小但更穩定的股票池）
        self.stock_pool = [
            # 核心大型股（流動性好，數據穩定）
            '2330', '2317', '2454', '2412', '2882', '2308', '2303', '2891',
            '2886', '6505', '2395', '2207', '3008', '2881', '2892', '1303',
            
            # 主要ETF（數據穩定，適合篩選）
            '0050', '0056', '006208', '00878', '00919', '00881',
            
            # 知名科技股
            '2376', '3034', '2379', '6446', '3443', '6415', '2408',
            
            # 穩定傳產股
            '1216', '2609', '2201', '1102', '2104', '2204', '2618'
        ]
        
        # 快取設定
        self.cache_timeout = 300  # 5分鐘快取
        self.max_retries = 3
        self.request_delay = 1  # 請求間隔1秒
    
    def calculate_rsi(self, prices, period=14):
        """計算RSI指標 - 適應性版本"""
        if len(prices) < 2:
            return 50  # 預設中性值
        
        # 調整週期以適應可用資料
        actual_period = min(period, len(prices) - 1, 10)
        if actual_period < 2:
            return 50
        
        try:
            deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
            gains = [delta if delta > 0 else 0 for delta in deltas]
            losses = [-delta if delta < 0 else 0 for delta in deltas]
            
            if len(gains) < actual_period:
                # 如果資料不足，使用簡化計算
                recent_gains = [g for g in gains if g > 0]
                recent_losses = [l for l in losses if l > 0]
                
                if not recent_gains and not recent_losses:
                    return 50
                
                avg_gain = sum(recent_gains) / len(recent_gains) if recent_gains else 0
                avg_loss = sum(recent_losses) / len(recent_losses) if recent_losses else 0
            else:
                avg_gain = sum(gains[:actual_period]) / actual_period
                avg_loss = sum(losses[:actual_period]) / actual_period
            
            if avg_loss == 0:
                return 100
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return round(max(0, min(100, rsi)), 2)
            
        except Exception:
            return 50  # 發生錯誤時回傳中性值
    
    def calculate_macd(self, prices):
        """計算MACD指標 - 適應性版本"""
        if len(prices) < 3:
            return 0, 0, 0  # 預設中性值
        
        try:
            # 簡化的MACD計算，適用於較少的資料點
            if len(prices) >= 12:
                # 使用標準MACD
                def ema(data, period):
                    multiplier = 2 / (period + 1)
                    ema_values = [data[0]]
                    for price in data[1:]:
                        ema_values.append((price * multiplier) + (ema_values[-1] * (1 - multiplier)))
                    return ema_values
                
                ema12 = ema(prices, min(12, len(prices) // 2))
                ema26 = ema(prices, min(26, len(prices) - 1))
                
                macd_line = ema12[-1] - ema26[-1]
                signal_line = macd_line * 0.8  # 簡化signal計算
                histogram = macd_line - signal_line
                
                return round(macd_line, 3), round(signal_line, 3), round(histogram, 3)
            else:
                # 使用價格趨勢作為MACD代替
                if len(prices) >= 3:
                    recent_trend = (prices[-1] - prices[-3]) / prices[-3] * 100
                    return round(recent_trend, 3), 0, round(recent_trend, 3)
                else:
                    return 0, 0, 0
                    
        except Exception:
            return 0, 0, 0
    
    def calculate_moving_averages(self, prices):
        """計算移動平均線 - 適應性版本"""
        if len(prices) < 2:
            current = prices[0] if prices else 0
            return current, current, current, current
        
        try:
            # 根據可用資料調整週期
            n = len(prices)
            
            ma5 = sum(prices[-min(5, n):]) / min(5, n)
            ma10 = sum(prices[-min(10, n):]) / min(10, n)
            ma20 = sum(prices[-min(20, n):]) / min(20, n)
            ma60 = sum(prices[-min(60, n):]) / min(60, n)
            
            return round(ma5, 2), round(ma10, 2), round(ma20, 2), round(ma60, 2)
            
        except Exception:
            current = prices[-1] if prices else 0
            return current, current, current, current
    
    def calculate_bollinger_bands(self, prices, period=20):
        """計算布林通道 - 適應性版本"""
        if len(prices) < 2:
            current = prices[0] if prices else 0
            return current, current, current
        
        try:
            # 調整週期以適應可用資料
            actual_period = min(period, len(prices))
            recent_prices = prices[-actual_period:]
            
            ma = sum(recent_prices) / actual_period
            
            if actual_period >= 3:
                variance = sum([(price - ma) ** 2 for price in recent_prices]) / actual_period
                std_dev = variance ** 0.5
                
                upper_band = ma + (2 * std_dev)
                lower_band = ma - (2 * std_dev)
            else:
                # 資料不足時使用簡化計算
                price_range = max(recent_prices) - min(recent_prices)
                upper_band = ma + price_range * 0.5
                lower_band = ma - price_range * 0.5
            
            return round(upper_band, 2), round(ma, 2), round(lower_band, 2)
            
        except Exception:
            current = prices[-1] if prices else 0
            return current, current, current
    
    def analyze_stock(self, stock_code, retries=0):
        """分析單一股票的技術指標 - 優化版"""
        try:
            print(f"📊 分析股票: {stock_code}")
            
            # 檢查快取
            cache_key = f"analysis_{stock_code}"
            cached_analysis = self.get_cache(cache_key)
            if cached_analysis:
                print(f"✅ 使用快取分析: {stock_code}")
                return cached_analysis
            
            # 延遲請求避免過於頻繁
            if retries > 0:
                time.sleep(self.request_delay * retries)
            
            # 獲取基本資訊
            basic_info = self.get_stock_info_with_retry(stock_code)
            if not basic_info or basic_info.get('錯誤'):
                print(f"❌ 無法獲取基本資訊: {stock_code}")
                return None
            
            # 獲取價格資料 - 進一步降低要求，提高成功率
            chart_data = self.get_chart_data_with_retry(stock_code, 14)  # 只要14天的資料
            if not chart_data or not chart_data.get('success'):
                print(f"❌ 無法獲取圖表資料: {stock_code}")
                return None
                
            data_points = chart_data.get('data', [])
            if len(data_points) < 5:  # 進一步降低最低資料要求
                print(f"❌ 資料點不足: {stock_code} ({len(data_points)} 點)")
                return None
            
            # 解析價格資料
            prices = []
            for item in data_points:
                try:
                    price = float(item['price'])
                    if price > 0:  # 確保價格有效
                        prices.append(price)
                except (ValueError, KeyError):
                    continue
            
            if len(prices) < 3:  # 進一步降低要求
                print(f"❌ 有效價格資料不足: {stock_code}")
                return None
            
            current_price = prices[-1]
            
            # 計算技術指標 - 安全版本
            analysis = {
                'stock_code': stock_code,
                'stock_name': basic_info.get('股票名稱', stock_code),
                'current_price': current_price,
                'analysis_time': datetime.now().isoformat()
            }
            
            # 計算價格變化（安全版本）
            analysis.update(self.calculate_price_changes(prices))
            
            # 計算技術指標（安全版本）
            analysis.update(self.calculate_technical_indicators(prices))
            
            # 解析成交量
            analysis['volume'] = self.parse_volume(basic_info.get('成交量', '0'))
            
            # 產生投資建議和評分
            analysis['signals'] = self.generate_signals(analysis)
            analysis['score'] = self.calculate_score(analysis)
            
            # 儲存快取
            self.save_cache(cache_key, analysis)
            
            print(f"✅ 成功分析: {stock_code} (評分: {analysis['score']})")
            return analysis
            
        except Exception as e:
            print(f"❌ 分析股票 {stock_code} 時發生錯誤: {e}")
            
            # 重試機制
            if retries < self.max_retries:
                print(f"🔄 重試分析 {stock_code} (第 {retries + 1} 次)")
                time.sleep(2 ** retries)  # 指數退避
                return self.analyze_stock(stock_code, retries + 1)
            
            return None
    
    def get_stock_info_with_retry(self, stock_code):
        """帶重試機制的股票資訊獲取"""
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    time.sleep(1 * attempt)
                return get_stock_basic_info(stock_code)
            except Exception as e:
                print(f"⚠️ 獲取 {stock_code} 基本資訊失敗 (嘗試 {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    return None
        return None
    
    def get_chart_data_with_retry(self, stock_code, days):
        """帶重試機制的圖表資料獲取"""
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    time.sleep(1 * attempt)
                return get_stock_chart_data(stock_code, days)
            except Exception as e:
                print(f"⚠️ 獲取 {stock_code} 圖表資料失敗 (嘗試 {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    return None
        return None
    
    def calculate_price_changes(self, prices):
        """計算價格變化 - 安全版本"""
        changes = {}
        try:
            if len(prices) > 1:
                changes['price_change_1d'] = round(((prices[-1] - prices[-2]) / prices[-2]) * 100, 2)
            else:
                changes['price_change_1d'] = 0
                
            if len(prices) > 5:
                changes['price_change_5d'] = round(((prices[-1] - prices[-6]) / prices[-6]) * 100, 2)
            else:
                changes['price_change_5d'] = 0
                
            if len(prices) > 20:
                changes['price_change_20d'] = round(((prices[-1] - prices[-21]) / prices[-21]) * 100, 2)
            else:
                changes['price_change_20d'] = 0
        except Exception as e:
            print(f"❌ 計算價格變化失敗: {e}")
            changes = {'price_change_1d': 0, 'price_change_5d': 0, 'price_change_20d': 0}
        
        return changes
    
    def calculate_technical_indicators(self, prices):
        """計算技術指標 - 安全版本"""
        indicators = {}
        
        try:
            # RSI
            indicators['rsi'] = self.calculate_rsi(prices) or 50
        except:
            indicators['rsi'] = 50
        
        try:
            # MACD
            macd, signal, histogram = self.calculate_macd(prices)
            indicators['macd'] = macd or 0
            indicators['signal'] = signal or 0
            indicators['histogram'] = histogram or 0
        except:
            indicators['macd'] = 0
            indicators['signal'] = 0
            indicators['histogram'] = 0
        
        try:
            # 移動平均線
            ma5, ma10, ma20, ma60 = self.calculate_moving_averages(prices)
            indicators['ma5'] = ma5 or prices[-1]
            indicators['ma10'] = ma10 or prices[-1]
            indicators['ma20'] = ma20 or prices[-1]
            indicators['ma60'] = ma60 or prices[-1]
        except:
            indicators['ma5'] = prices[-1] if prices else 0
            indicators['ma10'] = prices[-1] if prices else 0
            indicators['ma20'] = prices[-1] if prices else 0
            indicators['ma60'] = prices[-1] if prices else 0
        
        try:
            # 布林通道
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices)
            indicators['bb_upper'] = bb_upper or prices[-1]
            indicators['bb_middle'] = bb_middle or prices[-1]
            indicators['bb_lower'] = bb_lower or prices[-1]
        except:
            indicators['bb_upper'] = prices[-1] if prices else 0
            indicators['bb_middle'] = prices[-1] if prices else 0
            indicators['bb_lower'] = prices[-1] if prices else 0
        
        return indicators
    
    def parse_volume(self, volume_str):
        """解析成交量 - 安全版本"""
        try:
            if not volume_str or volume_str in ['N/A', '-', '']:
                return 0
            clean_volume = str(volume_str).replace(',', '').replace(' ', '')
            return int(clean_volume) if clean_volume.isdigit() else 0
        except:
            return 0
    
    def get_cache(self, key):
        """獲取快取資料"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # 檢查快取是否過期
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cache_time < timedelta(seconds=self.cache_timeout):
                    return cache_data['data']
        except Exception as e:
            print(f"❌ 讀取快取失敗: {e}")
        return None
    
    def save_cache(self, key, data):
        """儲存快取資料"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 儲存快取失敗: {e}")
    
    def generate_signals(self, analysis):
        """基於技術指標產生投資信號"""
        signals = []
        score = 0
        
        # RSI 信號
        rsi = analysis.get('rsi')
        if rsi:
            if rsi < 30:
                signals.append(("RSI超賣", "買進機會", "green"))
                score += 2
            elif rsi > 70:
                signals.append(("RSI超買", "注意風險", "red"))
                score -= 1
            elif 40 <= rsi <= 60:
                signals.append(("RSI中性", "持有觀望", "gray"))
        
        # MACD 信號
        macd = analysis.get('macd')
        signal = analysis.get('signal')
        if macd and signal:
            if macd > signal and analysis.get('histogram', 0) > 0:
                signals.append(("MACD黃金交叉", "買進信號", "green"))
                score += 2
            elif macd < signal and analysis.get('histogram', 0) < 0:
                signals.append(("MACD死亡交叉", "賣出信號", "red"))
                score -= 2
        
        # 移動平均線信號
        current_price = analysis.get('current_price', 0)
        ma5 = analysis.get('ma5')
        ma10 = analysis.get('ma10')
        ma20 = analysis.get('ma20')
        
        if ma5 and ma10 and ma20:
            if current_price > ma5 > ma10 > ma20:
                signals.append(("多頭排列", "強勢上漲", "green"))
                score += 3
            elif current_price < ma5 < ma10 < ma20:
                signals.append(("空頭排列", "弱勢下跌", "red"))
                score -= 3
            elif current_price > ma20:
                signals.append(("價格在月線上", "中性偏多", "yellow"))
                score += 1
        
        # 布林通道信號
        bb_upper = analysis.get('bb_upper')
        bb_lower = analysis.get('bb_lower')
        if bb_upper and bb_lower:
            if current_price <= bb_lower:
                signals.append(("觸及布林下軌", "超賣反彈", "green"))
                score += 1
            elif current_price >= bb_upper:
                signals.append(("觸及布林上軌", "超買回檔", "red"))
                score -= 1
        
        # 價格動能信號
        change_5d = analysis.get('price_change_5d', 0)
        if change_5d > 10:
            signals.append(("短期漲幅過大", "注意回檔", "orange"))
            score -= 1
        elif change_5d < -10:
            signals.append(("短期跌幅過大", "反彈機會", "blue"))
            score += 1
        
        return signals
    
    def calculate_score(self, analysis):
        """計算綜合評分 (0-100)"""
        score = 50  # 基準分數
        
        rsi = analysis.get('rsi', 50)
        macd = analysis.get('macd', 0)
        signal = analysis.get('signal', 0)
        current_price = analysis.get('current_price', 0)
        ma20 = analysis.get('ma20', 0)
        
        # RSI 評分
        if 30 <= rsi <= 70:
            score += 10
        elif rsi < 30:
            score += 15  # 超賣加分
        else:
            score -= 10  # 超買扣分
        
        # MACD 評分
        if macd > signal:
            score += 10
        else:
            score -= 5
        
        # 趨勢評分
        if ma20 and current_price > ma20:
            score += 15
        elif ma20 and current_price < ma20:
            score -= 10
        
        # 價格動能評分
        change_20d = analysis.get('price_change_20d', 0)
        if -5 <= change_20d <= 15:  # 溫和上漲
            score += 10
        elif change_20d < -20:  # 超跌
            score += 5
        elif change_20d > 30:  # 漲幅過大
            score -= 15
        
        return max(0, min(100, score))
    
    def screen_stocks(self, criteria=None):
        """執行股票篩選 - 優化版"""
        if criteria is None:
            criteria = {
                'min_rsi': 0,    # 放寬條件
                'max_rsi': 100,  # 放寬條件
                'min_score': 40, # 降低最低評分
                'price_trend': 'any',
                'volume_filter': False
            }
        
        # 確保條件合理
        criteria = self.validate_criteria(criteria)
        
        results = []
        processed = 0
        errors = 0
        
        print(f"🔍 開始篩選 {len(self.stock_pool)} 支股票...")
        print(f"📋 篩選條件: RSI({criteria['min_rsi']}-{criteria['max_rsi']}), 最低評分({criteria['min_score']})")
        
        # 隨機打亂股票順序，避免總是從同樣的股票開始
        import random
        shuffled_stocks = self.stock_pool.copy()
        random.shuffle(shuffled_stocks)
        
        for stock_code in shuffled_stocks:
            try:
                # 添加處理進度
                if processed % 3 == 0:
                    print(f"📊 已處理 {processed}/{len(self.stock_pool)} 支股票，找到 {len(results)} 支符合條件")
                
                analysis = self.analyze_stock(stock_code)
                processed += 1
                
                if analysis:
                    # 先檢查基本有效性
                    if self.is_valid_analysis(analysis):
                        # 再檢查是否符合篩選條件
                        if self.meets_criteria(analysis, criteria):
                            results.append(analysis)
                            print(f"✅ 找到符合條件股票: {stock_code} ({analysis['stock_name']}) - 評分: {analysis['score']}")
                            
                            # 如果已經找到足夠的結果，可以提前結束
                            if len(results) >= 20:
                                print(f"🎯 已找到 {len(results)} 支股票，提前結束篩選")
                                break
                else:
                    errors += 1
                
                # 減少延遲
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ 處理 {stock_code} 時發生錯誤: {e}")
                errors += 1
                continue
        
        # 依照評分排序
        if results:
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        print(f"✅ 篩選完成！")
        print(f"📊 處理股票: {processed} 支")
        print(f"❌ 錯誤數量: {errors} 支") 
        print(f"🎯 符合條件: {len(results)} 支")
        
        # 如果結果太少，提供建議
        if len(results) < 3:
            print("💡 建議: 結果較少，可以嘗試:")
            print("   - 降低最低評分要求")
            print("   - 放寬RSI範圍")
            print("   - 關閉成交量篩選")
        
        return results
    
    def validate_criteria(self, criteria):
        """驗證和修正篩選條件"""
        validated = criteria.copy()
        
        # RSI 範圍檢查
        validated['min_rsi'] = max(0, min(100, criteria.get('min_rsi', 0)))
        validated['max_rsi'] = max(0, min(100, criteria.get('max_rsi', 100)))
        
        # 確保最小值不大於最大值
        if validated['min_rsi'] > validated['max_rsi']:
            validated['min_rsi'], validated['max_rsi'] = validated['max_rsi'], validated['min_rsi']
        
        # 評分範圍檢查
        validated['min_score'] = max(0, min(100, criteria.get('min_score', 40)))
        
        # 趨勢檢查
        if criteria.get('price_trend') not in ['up', 'down', 'any']:
            validated['price_trend'] = 'any'
        
        return validated
    
    def is_valid_analysis(self, analysis):
        """檢查分析結果是否有效"""
        try:
            # 檢查必要欄位
            required_fields = ['stock_code', 'current_price', 'rsi', 'score']
            for field in required_fields:
                if field not in analysis or analysis[field] is None:
                    return False
            
            # 檢查數值合理性
            if analysis['current_price'] <= 0:
                return False
            
            if not (0 <= analysis['rsi'] <= 100):
                return False
            
            if not (0 <= analysis['score'] <= 100):
                return False
            
            return True
            
        except Exception:
            return False
    
    def meets_criteria(self, analysis, criteria):
        """檢查股票是否符合篩選條件 - 優化版"""
        if not analysis:
            return False
        
        try:
            # RSI 條件 - 更寬鬆的檢查
            rsi = analysis.get('rsi', 50)
            min_rsi = criteria.get('min_rsi', 0)
            max_rsi = criteria.get('max_rsi', 100)
            
            if not (min_rsi <= rsi <= max_rsi):
                return False
            
            # 評分條件
            score = analysis.get('score', 0)
            min_score = criteria.get('min_score', 0)
            
            if score < min_score:
                return False
            
            # 價格趨勢條件 - 更寬鬆
            price_trend = criteria.get('price_trend', 'any')
            if price_trend != 'any':
                change_5d = analysis.get('price_change_5d', 0)
                
                # 放寬趨勢判斷條件
                if price_trend == 'up' and change_5d < -5:  # 允許小幅下跌
                    return False
                elif price_trend == 'down' and change_5d > 5:  # 允許小幅上漲
                    return False
            
            # 成交量條件 - 更寬鬆
            if criteria.get('volume_filter', False):
                volume = analysis.get('volume', 0)
                if volume < 100:  # 降低最低成交量要求
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ 檢查篩選條件時發生錯誤: {e}")
            return False
    
    def get_preset_strategies(self):
        """預設選股策略 - 優化版"""
        return {
            'value_hunting': {
                'name': '價值獵人',
                'description': '尋找被低估的優質股票',
                'criteria': {
                    'min_rsi': 10,
                    'max_rsi': 60,
                    'min_score': 50,  # 降低評分要求
                    'price_trend': 'any',
                    'volume_filter': False  # 關閉成交量篩選
                }
            },
            'momentum': {
                'name': '動能追蹤', 
                'description': '捕捉上漲動能股票',
                'criteria': {
                    'min_rsi': 30,
                    'max_rsi': 80,
                    'min_score': 55,  # 降低評分要求
                    'price_trend': 'any',  # 改為不限制趨勢
                    'volume_filter': False
                }
            },
            'oversold_bounce': {
                'name': '超跌反彈',
                'description': '尋找超跌後的反彈機會',
                'criteria': {
                    'min_rsi': 0,
                    'max_rsi': 40,
                    'min_score': 40,  # 降低評分要求
                    'price_trend': 'any',
                    'volume_filter': False
                }
            },
            'stable_growth': {
                'name': '穩健成長',
                'description': '尋找穩定成長的股票',
                'criteria': {
                    'min_rsi': 20,
                    'max_rsi': 80,
                    'min_score': 55,  # 降低評分要求
                    'price_trend': 'any',
                    'volume_filter': False
                }
            },
            'all_stocks': {
                'name': '全部股票',
                'description': '顯示所有可分析的股票',
                'criteria': {
                    'min_rsi': 0,
                    'max_rsi': 100,
                    'min_score': 0,  # 最低要求
                    'price_trend': 'any',
                    'volume_filter': False
                }
            }
        }

