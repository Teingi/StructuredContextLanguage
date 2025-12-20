import os
import json
from openai import OpenAI
from function_reg import getTools,call_function_safe

def send_messages(client, model, messages,tools):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

def function_call_playground(client, model, messages, tools):    
    response = send_messages(client, model, messages, tools)
    # todo, feedback loop model(langchain)
    print(response)
    for tool_call in response.tool_calls:
        func1_name = tool_call.function.name
        func1_args = tool_call.function.arguments
        print(func1_name)
        print(func1_args)
        args_dict = json.loads(func1_args)
        func1_out = call_function_safe(func1_name,args_dict)

        messages.append(response)
        messages.append({
            'role': 'tool',
            'content': f'{func1_out}',
            'tool_call_id': tool_call.id
        })
    # print(messages)
    response = send_messages(client, model, messages, tools)
    return response.content
  
## init for test
client = OpenAI(
    api_key=os.getenv("API_KEY",""),
    base_url=os.getenv("BASE_URL","")
)
model = os.getenv("MODEL","")
messages = [{'role': 'user', 'content': "用中文回答：strawberry中有多少个r?"}]

print(function_call_playground(client, model, messages, getTools("用中文回答：strawberry中有多少个r?")))
messages = [{'role': 'user', 'content': "用中文回答：9.11和9.9，哪个小?"}]

print(function_call_playground(client, model, messages, getTools("用中文回答：9.11和9.9，哪个小?")))