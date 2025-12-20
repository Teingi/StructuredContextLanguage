import os
import json
from openai import OpenAI
from function_reg import FunctionRegistry
from scl.embeddings.impl import OpenAIEmbedding
from scl.storage.pg import PgVectorFunctionStore

def send_messages(client, model, messages,registry):
    tools = registry.getTools(messages[0]['content'])
    print(tools)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

def function_call_playground(client, model, messages, registry):    
    response = send_messages(client, model, messages, registry)
    # todo, feedback loop model(langchain)
    print(response)
    for tool_call in response.tool_calls:
        func1_name = tool_call.function.name
        func1_args = tool_call.function.arguments
        print(func1_name)
        print(func1_args)
        args_dict = json.loads(func1_args)
        func1_out = registry.call_function_safe(func1_name,args_dict)

        messages.append(response)
        messages.append({
            'role': 'tool',
            'content': f'{func1_out}',
            'tool_call_id': tool_call.id
        })
    # print(messages)
    response = send_messages(client, model, messages, registry)
    return response.content
  
## init for test
client = OpenAI(
    api_key=os.getenv("API_KEY",""),
    base_url=os.getenv("BASE_URL","")
)
model = os.getenv("MODEL","")

function_store = PgVectorFunctionStore(
            dbname="postgres",
            user="postgres",
            password="postgres",  # 请修改为您的密码
            host="localhost",
            port="5432",
            embedding_service=OpenAIEmbedding()
        )
registry = FunctionRegistry(function_store, True)

registry.insert_function(
    function_name="add",
    function_body="""
def add(a: float, b: float):
    return a + b
""",
    llm_description={'type': 'function',
    'function': {
        'name': 'add',
        'description': 'Compute the sum of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'integer',
                    'description': 'A number',
                },
                'b': {
                    'type': 'integer',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
},
    function_description="计算两数之和"
)

registry.insert_function(
    function_name="mul",
    function_body="""
def mul(a: float, b: float):
    return a * b
""",
    llm_description={'type': 'function',
    'function': {
        'name': 'mul',
        'description': 'Calculate the product of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'integer',
                    'description': 'A number',
                },
                'b': {
                    'type': 'integer',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
},
    function_description="计算两数之积"
)

registry.insert_function(
    function_name="count_letter",
    function_body="""
def count_letter(text, letter):
    return text.count(letter)
""",
    llm_description={'type': 'function',
    'function': {
        'name': 'count_letter',
        'description': 'Count the number of times a letter appears in a text',
        'parameters': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': 'The text to search in',
                },
                'letter': {
                    'type': 'string',
                    'description': 'The letter to count',
                },
            },
            'required': ['text', 'letter'],
        },
    }
},
    function_description="计算字母在单词中出现的次数"
)


registry.insert_function(
    function_name="compare",
    function_body="""
def compare(a: float, b: float):
    if a > b:
        return f'{a} is greater than {b}'
    elif a < b:
        return f'{b} is greater than {a}'
    else:
        return f'{a} is equal to {b}'
""",
    llm_description={'type': 'function',
    'function': {
        'name': 'compare',
        'description': 'Compare two number, which one is bigger',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'number',
                    'description': 'A number',
                },
                'b': {
                    'type': 'number',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
},
    function_description="比较两个数字，哪个更大"
)

messages = [{'role': 'user', 'content': "用中文回答：单词strawberry中有多少个字母r?"}]
print(function_call_playground(client, model, messages, registry))
messages = [{'role': 'user', 'content': "用中文回答：9.11和9.9，哪个小?"}]
print(function_call_playground(client, model, messages, registry))