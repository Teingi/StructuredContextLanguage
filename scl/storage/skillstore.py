import sys
import os
import json
import logging
import hashlib
from pathlib import Path
import numpy as np

from typing import Optional, List, Dict, Any
# Add the StructuredContextLanguage directory to the path
scl_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(scl_root)

from scl.trace import tracer
from scl.embeddings.impl import OpenAIEmbedding
from scl.storage.base import FunctionStoreBase

# Import from the local skills_ref module
from scl.storage.skills_ref.parser import read_properties
from scl.storage.skills_ref.models import SkillProperties


class SkillStore(FunctionStoreBase):
    def __init__(self, folder, embedding_service=None):
        super().__init__()
        self.folder = folder
        self.embedding_service = embedding_service

    def cosine_similarity(self, vec1, vec2):
        """
        计算两个向量的余弦相似度
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        
        similarity = dot_product / (norm_vec1 * norm_vec2)
        return float(similarity) 

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
        result = {}
        query_embedding = self.generate_embedding(query_text)
        dir_path = Path(self.folder).resolve()
        for item in dir_path.iterdir():
            logging.info(f"Processing {item} for skill")
            print(f"Processing {item} for skill")
            if item.is_dir():
                try:
                    skill_props = read_properties(item)
                    logging.info(f"skill found {skill_props.name}")
                    print(f"skill found {skill_props.name}")
                    skill_embedding = self.generate_embedding(skill_props.description)
                    print(self.cosine_similarity(query_embedding, skill_embedding))
                    result[str(item)] = skill_props
                except Exception as e:
                    print(f"Error reading properties for {item}: {e}")
                    logging.error(f"Error reading properties for {item}: {e}")
        #print(result)
        return result    


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

def main():
    skill_store = SkillStore(folder="./skills/skills",embedding_service=OpenAIEmbedding())
    skill_store.search_by_similarity("Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration.")

if __name__ == "__main__":
    main()