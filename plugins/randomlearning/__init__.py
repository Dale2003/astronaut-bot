import os
import random
from PIL import Image
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.permission import GROUP_MEMBER,PRIVATE,GROUP
import pandas as pd
import sys

# 文件路径
if getattr(sys, 'frozen', False):
    current_file_path = sys.executable
else:
    current_file_path = __file__
current_file_dir = os.path.dirname(current_file_path)

excel_file = pd.ExcelFile(os.path.join(current_file_dir, 'learning.xlsx'))

# 读取Excel文件
df = pd.read_excel(excel_file, sheet_name='Sheet1')

def random_meal():
    # 将DataFrame转为字典，其中key为食堂名称，value为菜品列表
    canteens = df.set_index(df.columns[0]).T.to_dict('list')

    # 去除每个菜品列表中的空值
    for key in canteens.keys():
        canteens[key] = [x for x in canteens[key] if pd.notna(x)]

    # 随机选择食堂
    canteen = random.choice(list(canteens.keys()))

    # 随机选择食堂中的菜品
    dish = random.choice(canteens[canteen])

    res = '建议您去'+ str(canteen) + '的' + str(dish) + '自习捏~'
    return res

guess = on_command("去哪自习", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)

@guess.handle()
async def handle_function():
    global res
    res = random_meal()
    await guess.send(res)