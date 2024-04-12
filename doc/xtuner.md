# 列出所有内置配置
xtuner list-cfg

# 微调模型
nohup xtuner train internlm_chat_7b_qlora_self.py --deepspeed deepspeed_zero2 > nohup.out 2>&1 & 

# PTH模型转换为 HuggingFace 模型
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU
xtuner convert pth_to_hf ./internlm_chat_7b_qlora_self.py ./work_dirs/internlm_chat_7b_qlora_self/epoch_1.pth ./hf

# 模型合并
xtuner convert merge ./internlm-chat-7b ./hf ./merged --max-shard-size 2GB

# 模型对话
xtuner chat ./merged  --prompt-template internlm_chat

