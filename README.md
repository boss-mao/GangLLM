## 项目介绍
- GangLLM 是一个专门与用户抬杠的大模型，根据用户的输入会进行杠精式的回复，该模型能够捕捉到用户言辞中的细微漏洞，并据此展开犀利的反驳，该模型在开源大模型上微调而来，基础模型采用的InternLLM-Chat-7B模型，采用1680条杠精式对话数据，外加100条自我认知数据进行的微调训练。

- **特别注意，心脏不好或者有心理疾病者慎用，因使用本模型后产生的心理或生理问题，本人概不负责。**
- 欢迎大家star~⭐⭐

## 效果演示
<video controls>  
  <source src="./doc/asset/demo.mp4" type="video/mp4">  
  Your browser does not support the video tag.  
</video>

## 在线体验
- 体验地址：筹备中，敬请期待
- 模型文件：https://openxlab.org.cn/models/detail/cat_boss/GangLLM

## 更多资讯
- 请扫码关注微信公众号或者微信搜索“科技猫老板”，了解更多大模型相关技术。

<p align="center">
<img src="./doc/asset/qrcode.jpg " alt="示例图片的标题">
</p>

## 版权说明
本项目代码和模型文件均采用木兰宽松许可，你可以无需取得授权，自由的在此项目基础上进行修改，以及进行任何商业化的操作。

## 特别鸣谢
- [上海人工智能实验室](https://www.shlab.org.cn/)

---
## 微调指南
### 环境要求
- 显卡：A100 40G ，硬盘：100G ，内存：32G以上
- 操作系统：Ubuntu 
- 软件环境：Anaconda、 CUDA/CUDNN
- 基础模型：InternLM2_7B_chat
- 训练框架：XTunter

### 环境安装
- 安装依赖
```
python -m pip install --upgrade pip
pip install modelscope==1.9.5
pip install transformers==4.35.2
pip install streamlit==1.24.0
pip install sentencepiece==0.1.99
pip install accelerate==0.24.1
```
- 安装XTunter
```
  cd  GangLLM/xtuner
  pip install -e '.[all]'
```

### 准备数据
#### 原始数据
- 弱智吧帖子数据集，https://github.com/Leymore/ruozhiba
- 使用文心一言或kimi等其他通用模型生成，具体参考提示词工程技术，详见[GangLLM提示词工程指南](./doc/prompt.md)

#### 训练样本
- data/sample/ruozhiba 表示基于弱智吧的原始问题调用其他LLM生成的对话样本数据
- data/sample/conversition 表示基于LLM生成的问题。再调用其他LLM生成的对话数据集
- data/sample/self 表示采用数据增强后的自我认知数据集
- dataset.json表示以上三部分合成后的数据集，最终训练使用的数据集

### 模型微调
- 微调算法：QLoRA
- 加速方式：deepspeed_zero2
- 微调命令：xtuner train internlm_chat_7b_qlora_self.py --deepspeed deepspeed_zero2,
详见[xtuner命令](./doc/xtuner.md)

### 部署指南
- 第一种方式，python cli_demo.py
- 第二种方式，xtuner chat ./merged  --prompt-template internlm_chat


