from utils import *

## function name, function body, function description, function metadata
FUNCTION_REGISTRY = {
    'add': add,
    'mul': mul, 
    'compare': compare,
    'count_letter_in_string': count_letter_in_string
}
## RAG search between context and function description after embedding
## Return function in openAI tool format
def getTools(context: str):
    return tools

def call_function_safe(func_name: str, args_dict=None):
    """
    通过注册表安全地调用函数
    """
    func = FUNCTION_REGISTRY.get(func_name)
    
    if func is None:
        raise ValueError(f"Function '{func_name}' is not registered or does not exist")
    
    # 调用函数
    return func(**args_dict)
