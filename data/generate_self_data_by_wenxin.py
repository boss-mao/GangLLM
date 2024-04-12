import requests
import json
import logging  
import re  
import os


# 文心一言KEY
ERNIE_API_KEY = os.getenv('ERNIE_API_KEY')
# 文心一言SECRET
ERNIE_SECRET_KEY = os.getenv('ERNIE_SECRET_KEY')

DATA_FILE_NAME_TEMPLATE="./sample-self/data.json"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": ERNIE_API_KEY, "client_secret": ERNIE_SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def send_message_to_wenxin(token,content):  
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + token
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "temperature": 1,
        "disable_search": True,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def generate_data_by_wenxin(token):
    prompt= '''角色：你目前扮演一个互联网杠精。  
               背景信息: 杠精的特点有：喜欢反驳、无视或曲解逻辑、钻牛角尖、讽刺挖苦、不关注事实、自我中心。
                目标：1.请用杠精的方式对以下对话内容进行数据增强，不改变原意，增强到10条
                            正常提问者：你是谁？
                            杠精：我是专业的抬杠艺术家，不服来论辩。
                      2. 严格遵循, 请以如下格式返回生成的数据, 只返回JSON格式，json模板:  
                            [  
                                {
                                    "input":"AAA","output":"BBBB" 
                                }
                            ]
            '''
        
    response_json_str=send_message_to_wenxin(token,prompt)
    response_obj=json.loads(response_json_str)
    result_json_str=str(response_obj["result"]).replace("```json","").replace("```","").replace(" ","").replace("\r","").replace("\n","")
    result_json_str = re.sub(r'\r?\n', ' ', result_json_str)

    try:
        result_item=json.loads(result_json_str)
        self_data_list=[]
        for item in result_item:
            self_data_list.append({"conversation":[item]})
        return self_data_list
    except Exception  as exception:
        logging.error("解析json异常:%s, 内容：%s",str(exception),result_json_str)
        return []

def store_data(result_list): 
    with open(DATA_FILE_NAME_TEMPLATE, 'w',encoding="utf-8") as file:  
        json.dump(result_list, file, ensure_ascii=False, indent=4)

def main():
    logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s',  
                    filename='app.log',
                    filemode='a')
    

    token=get_access_token()
    result_list=[]
    for i in range(10):
        result=generate_data_by_wenxin(token)
        result_list.extend(result)

    store_data(result_list)
    logging.info('generta slef data ：%d',len(result_list))
    
if __name__ == '__main__':
    main()
 
    





