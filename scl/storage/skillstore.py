import sys
import os
import json
import logging
import hashlib
from typing import Optional, List, Dict, Any
# Add the StructuredContextLanguage directory to the path
scl_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(scl_root)

from scl.trace import tracer
from .base import FunctionStoreBase


class SkillStore(FunctionStoreBase):
    def __init__(self, folder, embedding_service=None):
        self.folder = folder
        self.embedding_service = embedding_service
        
    @tracer.start_as_current_span("generate_embedding")
    def generate_embedding(self, text):
        """生成文本的嵌入向量"""
        embedding = self.embedding_service.embed(text)
            # Convert to Vector type if available
        return embedding

    @tracer.start_as_current_span("insert_function")
    def insert_function(self, function_name, function_body, llm_description, function_description):
        pass

    @tracer.start_as_current_span("update_function")
    def update_function(self, function_id=None, function_name=None, function_body=None, llm_description=None, function_description=None):
        pass

    @tracer.start_as_current_span("get_function_by_name")
    def get_function_by_name(self, function_name):
        """根据函数名查询"""
        # todo
        pass

    @tracer.start_as_current_span("search_by_similarity")
    def search_by_similarity(self, query_text, limit=5, min_similarity=0.5):
        """根据描述相似度查询函数"""
        # todo
        pass

    @tracer.start_as_current_span("delete_function")
    def delete_function(self, function_id=None, function_name=None):
        # no implementation
        pass
    
    @tracer.start_as_current_span("list_all_functions")
    def list_all_functions(self, limit=10):
        # todo
        pass

    def support_function_Call(self) -> bool:
        return False
