"""
RAG (Retrieval-Augmented Generation) 系統
支援多種RAG實現方式和金融股票資料查詢
"""

__version__ = "1.0.0"
__author__ = "Financial Web App"

# 導入核心RAG類別
from .core.advanced_rag import AdvancedRAGSystem
from .core.lightweight_rag import LightweightRAGSystem  
from .core.simple_rag import SimpleRAGSystem
from .core.rag_system import RAGSystem

__all__ = [
    'AdvancedRAGSystem',
    'LightweightRAGSystem', 
    'SimpleRAGSystem',
    'RAGSystem'
] 