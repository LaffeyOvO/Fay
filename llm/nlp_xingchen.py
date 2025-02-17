import requests
import json
from utils import util, config_util
from core import content_db

def question(cont, uid=0, observation=""):
    url = 'https://nlp.aliyuncs.com/v2/api/chat/send'

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'X-AcA-DataInspection': 'disable',
        'x-fag-servicename': 'aca-chat-send',
        'x-fag-appcode': 'aca',
        'Authorization': f"Bearer {config_util.key_xingchen_api_key}"
    }
    contentdb = content_db.new_instance()
    if uid == 0:
        communication_history = contentdb.get_list('all','desc', 11)
    else:
        communication_history = contentdb.get_list('all','desc', 11, uid)
    #历史记录处理
    message=[]
    i = len(communication_history) - 1
    
    if len(communication_history)>1:
        while i >= 0:
            answer_info = dict()
            if communication_history[i][0] == "member":
                answer_info["role"] = "user"
                answer_info["content"] = communication_history[i][2]
            elif communication_history[i][0] == "fay":
                answer_info["role"] = "assistant"
                answer_info["content"] = communication_history[i][2]
            message.append(answer_info)
            i -= 1
    else:
         answer_info = dict()
         answer_info["role"] = "user"
         answer_info["content"] = cont
         message.append(answer_info)
    data = {
        "input": {
            "messages": message,
            "aca": {
                "botProfile": {
                    "characterId": config_util.xingchen_characterid,
                    "version": 1
                },
                "userProfile": {
                    "userId": "1234567891",
                    "userName": "我",
                    "basicInfo": ""
                },
                "scenario": {
                    "description": "你是数字人Fay。用户问你问题的时候回答之前请一步一步想清楚。你的底层AI算法技术是Fay。"
                },
                "context": {
                    "useChatHistory": False,
                    "isRegenerate": False,
                }
            }
        },
        "parameters": {
            "seed": 1683806810,
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if response_data.get('success') and 'data' in response_data and 'choices' in response_data['data'] and len(response_data['data']['choices']) > 0:
                content = response_data['data']['choices'][0]['messages'][0]['content']
                return content
            else:
                util.log(1, "通义星辰调用失败，请检查配置")
                response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"
                return response_text
        else:
            util.log(1, f"通义星辰调用失败，请检查配置（错误码：{response.status_code}）")
            response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"
            return response_text
    except Exception as e:
        util.log(1, f"通义星辰调用失败，请检查配置（错误：{e}）")
        response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"
        return response_text

# # 调用函数测试
# result = question("你早")
# if result:
#     print(f"Received response: {result}")
# else:
#     print("Failed to get a valid response.")