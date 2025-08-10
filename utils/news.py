import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin
from typing import List, Dict, Optional

# 复用 twse 的設定與快取
try:
    from utils.twse import HEADERS, CONFIG, get_cache, save_cache
except Exception:
    # 後備：若無法匯入，提供最基本的設定，快取降級為無
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    }
    CONFIG = {'timeout': 15}

    def get_cache(key: str):
        return None

    def save_cache(key: str, data):
        return None


def _relative_time_string(published_dt: Optional[datetime]) -> str:
    if not published_dt:
        return '剛剛'
    try:
        delta = datetime.now() - published_dt
        if delta < timedelta(minutes=1):
            return '剛剛'
        if delta < timedelta(hours=1):
            mins = int(delta.total_seconds() // 60)
            return f'{mins}分鐘前'
        if delta < timedelta(days=1):
            hours = int(delta.total_seconds() // 3600)
            return f'{hours}小時前'
        days = delta.days
        return f'{days}天前'
    except Exception:
        return '剛剛'


def _parse_rss_datetime(text: str) -> Optional[datetime]:
    # RSS 常見格式: Wed, 17 Jul 2025 12:34:56 +0800
    for fmt in [
        '%a, %d %b %Y %H:%M:%S %z',
        '%a, %d %b %Y %H:%M:%S %Z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S%Z',
    ]:
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            continue
    return None


def _fetch_from_rss(rss_url: str) -> List[Dict]:
    items: List[Dict] = []
    try:
        resp = requests.get(rss_url, timeout=CONFIG.get('timeout', 15), headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'xml')
        for item in soup.find_all('item'):
            title_tag = item.find('title')
            link_tag = item.find('link')
            pub_tag = item.find('pubDate')
            title = (title_tag.text or '').strip() if title_tag else ''
            link = (link_tag.text or '').strip() if link_tag else ''
            pub_dt = _parse_rss_datetime(pub_tag.text.strip()) if pub_tag and pub_tag.text else None
            if title and link:
                items.append({
                    'title': title,
                    'link': link,
                    'published_at': pub_dt.isoformat() if pub_dt else None,
                    'relative_time': _relative_time_string(pub_dt),
                    'source': 'Yahoo',
                })
    except Exception:
        pass
    return items


def _fetch_from_html(list_url: str) -> List[Dict]:
    items: List[Dict] = []
    try:
        resp = requests.get(list_url, timeout=CONFIG.get('timeout', 15), headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')

        # 盡量通用地抓取文章連結（/news/slug）
        seen = set()
        for a in soup.select('a'):
            href = a.get('href') or ''
            text = (a.get_text() or '').strip()
            if not text or len(text) < 8:
                continue
            if '/news/' in href:
                link = href
                if href.startswith('/'):
                    link = urljoin('https://tw.stock.yahoo.com', href)
                # 過濾重複與非新聞
                key = (text, link)
                if key in seen:
                    continue
                seen.add(key)
                items.append({
                    'title': text,
                    'link': link,
                    'published_at': None,
                    'relative_time': '最新',
                    'source': 'Yahoo',
                })
            if len(items) >= 20:
                break
    except Exception:
        pass
    return items


def get_yahoo_stock_top_news(limit: int = 3) -> List[Dict]:
    """抓取 Yahoo 股市/財經熱門新聞，回傳最多 limit 筆。
    回傳欄位：title, link, relative_time, source
    具備本地快取（預設 5 分鐘，沿用 twse.CONFIG['cache_duration']）。
    """
    cache_key = 'yahoo_stock_news'
    cached = get_cache(cache_key)
    if cached and isinstance(cached, list):
        return cached[:limit]

    candidates: List[Dict] = []

    # 優先 RSS（較穩定）
    rss_candidates = [
        'https://tw.news.yahoo.com/rss/finance',  # Yahoo 台灣 財經 RSS
    ]
    for url in rss_candidates:
        candidates.extend(_fetch_from_rss(url))
        if len(candidates) >= limit:
            break

    # 後備：解析 Yahoo 股市新聞頁
    if len(candidates) < limit:
        html_candidates = [
            'https://tw.stock.yahoo.com/news',
        ]
        for url in html_candidates:
            candidates.extend(_fetch_from_html(url))
            if len(candidates) >= limit:
                break

    # 去重（以標題+連結）
    deduped: List[Dict] = []
    seen_pairs = set()
    for n in candidates:
        key = (n.get('title'), n.get('link'))
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        deduped.append(n)
        if len(deduped) >= limit:
            break

    # 快取
    save_cache(cache_key, deduped)
    return deduped


