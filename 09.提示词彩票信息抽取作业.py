from openai import OpenAI
from pyexpat.errors import messages
import json

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

schema = ["期数", "中奖号码", "中奖等级"]

example_data = [
    {
        "content": "2025年第100期，开好红球22 21 06 01 03 11 篮球 07，一等奖中奖为2注。",
        "answers": {"期数": "2025100", "中奖号码": [1, 3, 6, 11, 21, 22, 7], "一等奖": "2注"}
    },
    {
        "content": "2025101期，有3注1等奖，10注2等奖，开号篮球11，中奖红球3、5、7、11、12、16。",
        "answers": {"期数": "2025101", "中奖号码": [3, 5, 7, 11, 12, 16, 11], "一等奖": "3注"}
    }
]

questions = [
    "2026年第1034期，开好红球22 17 26 01 03 11 篮球 21，二等奖中奖为2注。",
    "2025101期，有3注1等奖，11注2等奖，开号篮球11，中奖红球3、5、7、11、22、16。"
]

"""
[
    {"role": "system",     "content": f"你帮我完成信息抽取，我给你句子，你抽取{schema}信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："}，
    {"role": "user",       "content": "2025年第100期，开好红球22 21 06 01 03 11 篮球 07，一等奖中奖为2注。"},
    {"role": "assistant",  "content": '{"期数": "2025101", "中奖号码": [3, 5, 7, 11, 12, 16, 11], "一等奖": "3注"}'},
    {"role": "user",       "content": "2025101期，有3注1等奖，10注2等奖，开号篮球11，中奖红球3、5、7、11、12、16。"},
    {"role": "assistant",  "content": '{"期数": "2025101", "中奖号码": [3, 5, 7, 11, 12, 16, 11], "一等奖": "3注"}'},
    
    {"role": "user",       "content": f"按照上述示例，现在抽取这个句子的信息：{要抽取的句子文本}"}
]
"""

messages = [
    {"role": "system", "content": f"你帮我完成信息抽取，我给你句子，你抽取{schema}信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："}
]

for example in example_data:
    messages.append({"role": "user", "content": example["content"]})
    messages.append({"role": "assistant", "content": json.dumps(example["answers"], ensure_ascii=False)})

# for x in messages:
#     print(x)

for q in questions:
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages + [{"role": "user", "content": f"按照上述示例，现在抽取这个句子的信息：{q}"}]
    )
    print(response.choices[0].message.content)