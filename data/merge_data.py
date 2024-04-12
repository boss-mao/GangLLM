import os
import json
import random
merge_dataset=[]

def store_dataset(merge_dataset): 
    with open('./sample/dataset.json', 'w',encoding="utf-8") as file:  
        json.dump(merge_dataset, file, ensure_ascii=False, indent=4)

for sample_dir in ['./sample/conversition','./sample/ruozhiba','./sample/self']:
    for root, dirs, files in os.walk(sample_dir):  
        for file in files:  
            # 构建文件的完整路径  
            file_path = os.path.join(root, file)  
            # 读取文件内容  
            with open(file_path, 'r', encoding='utf-8') as f:  
                content = f.read()  
                conversation_list=json.loads(content)
                merge_dataset.extend(conversation_list)
                print("合并数据集{}:{}条".format(file_path,len(conversation_list)))

random.shuffle(merge_dataset)  
store_dataset(merge_dataset)
print("合并数据集总数:{}条".format(len(merge_dataset)))