import requests
import json
import logging  
import re  
import os


# 文心一言KEY
ERNIE_API_KEY = os.getenv('ERNIE_API_KEY')
# 文心一言SECRET
ERNIE_SECRET_KEY = os.getenv('ERNIE_SECRET_KEY')

# 对话的数据分片数量，达到该数据规模进行分片存储,防止脚本奔溃后数据丢失
STROE_SHARD_COUNT=10
#从第几个问题开始处理
QUESTION_START_INDEX=871
#结束问题索引
QUESTION_END_INDEX=1000
#文件命名 开始问题索引+结束问题索引+分片标号
DATA_FILE_NAME_TEMPLATE="./sample/ruozhiba/data_{}_{}_{}.json"

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

def generate_data_by_wenxin(token,question):
    prompt= f''' 目标：你目前扮演一个互联网杠精、键盘侠、喜欢用怼人、讽刺的方式回复问题。  
                 输出要求：1. 请根据我输入的场景，构造一个连续的多轮对话记录。  
                          2. 对话内容尽量采用疑问句，双方不关心对方表达的主要内容，寻找语言的细节漏洞，不断反驳对方观点。
                          3. 严格遵循, 请以如下格式返回生成的数据, 只返回JSON格式，json模板:  
                            [  
                                {{  
                                    "input":"AAA","output":"BBBB" 
                                }} 
                            ]  
                 场景：{question}'''
        
    response_json_str=send_message_to_wenxin(token,prompt)
    response_obj=json.loads(response_json_str)
    result_json_str=str(response_obj["result"]).replace("```json","").replace("```","").replace(" ","").replace("\r","").replace("\n","")
    result_json_str = re.sub(r'\r?\n', ' ', result_json_str)

    try:
        result_item=json.loads(result_json_str)
        conversation_data={"conversation":result_item}
        return [conversation_data]
    except Exception  as exception:
        logging.error("解析json异常:%s, 内容：%s",str(exception),result_json_str)
        return []

def store_data(store_shard_index,result_list): 
    with open(DATA_FILE_NAME_TEMPLATE.format(QUESTION_START_INDEX,QUESTION_END_INDEX,store_shard_index), 'w',encoding="utf-8") as file:  
        json.dump(result_list, file, ensure_ascii=False, indent=4)

def read_question_list_from_file():
    question_list=[]
    with open('./raw/ruozhiba/question.txt', 'r',encoding='utf-8') as file:   
        content = file.read()  
        question_list=content.split('\n')

    return question_list

def main():
    logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s',  
                    filename='app.log', # 日志文件名，如果没有这个参数，日志输出到console  
                    filemode='a')
    
    question_list=read_question_list_from_file()
    global QUESTION_END_INDEX
    if len(question_list) < QUESTION_END_INDEX:
        QUESTION_END_INDEX = len(question_list)

    question_list=question_list[QUESTION_START_INDEX:QUESTION_END_INDEX]

    token=get_access_token()
    result_list=[]
    store_shard_index = 0
    for index,question in enumerate(question_list):
        logging.info("porcess question index : %d",QUESTION_START_INDEX+index)

        result=generate_data_by_wenxin(token,question)
        result_list.extend(result)

        if len(result_list) >= STROE_SHARD_COUNT:
            store_data(store_shard_index,result_list) 
            store_shard_index=store_shard_index+1
            result_list=[]

    if len(result_list)>0:
        store_data(store_shard_index,result_list)
    
if __name__ == '__main__':
    main()
 
    





