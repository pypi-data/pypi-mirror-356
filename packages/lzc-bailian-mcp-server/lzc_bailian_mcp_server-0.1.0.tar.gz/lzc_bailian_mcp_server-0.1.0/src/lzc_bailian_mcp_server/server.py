# -*- coding: utf-8 -*-
import json
import os
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import requests
import os
import logging
import dashscope
logger = logging.getLogger('mcp')
settings = {
    'log_level': 'DEBUG'
}


ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
BOT_ID = os.getenv("BOT_ID")
# 初始化mcp服务
mcp = FastMCP('lzc-bailian-mcp-server', log_level='ERROR', settings=settings)
# 定义工具


def chat(content):
    url = "https://api.coze.cn/v3/chat"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "bot_id": BOT_ID,
        "user_id": "123456789",
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": content,
                "content_type": "text"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def retrieve(chat_id,conversation_id):
    url = 'https://api.coze.cn/v3/chat/retrieve'
    params = {
        'chat_id': chat_id,
        'conversation_id': conversation_id
    }
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()

def list_message(chat_id,conversation_id):
    url = f"https://api.coze.cn/v3/chat/message/list?chat_id={chat_id}&conversation_id={conversation_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

@mcp.tool(name='滴灌通助手', description='滴灌通客服助手，回答用户问题')
async def describe_MIFC(
        query: str = Field(description='用户问题')
) -> str:
    """

    :param query:
    :return:
    """
    chat_rsp = chat(query)
    if chat_rsp['code'] == 0:
        chat_id = chat_rsp['data']['id']
        conversation_id = chat_rsp['data']['conversation_id']
        completed =  False
        while not completed:
            retrieve_rsp = retrieve(chat_id,conversation_id)
            if retrieve_rsp['code'] == 0:
                chatV3ChatDetail = retrieve_rsp['data']
                status = chatV3ChatDetail['status']
                if status == 'completed':
                    completed = True
                    messages = list_message(chat_id,conversation_id)
                    if messages['code'] == 0:
                        chatV3MessageDetail= messages['data']
                        for item in chatV3MessageDetail:
                            if item['type'] == 'answer':
                                print(item['content'])
                                return item['content']

        return "生成回答出现问题"
    return "生成回答出现问题"


def run():
    mcp.run(transport='stdio')
if __name__ == '__main__':
    run()

