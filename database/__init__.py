"""
Database 模組 - 資料庫相關功能
包含模型定義、資料庫工具和管理腳本
"""

from .models import db, User, Watchlist, SearchHistory, PriceAlert

__version__ = "1.0.0"

__all__ = [
    'db',
    'User', 
    'Watchlist',
    'SearchHistory',
    'PriceAlert'
] 