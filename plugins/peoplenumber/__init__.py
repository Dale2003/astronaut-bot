import os
import random
import wave
import contextlib
import json
from datetime import datetime
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.permission import GROUP_MEMBER,PRIVATE,GROUP
from nonebot.matcher import Matcher

import re

guess = on_command("人数", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)

@guess.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):  
    if args.extract_plain_text():
        matcher.set_arg("place_number", args)

@guess.got("place_number", f"若想上报人数，请输入机厅缩写（一个汉字）和人数（一个数字），如“万3”；若想查询人数请输入机厅缩写和几，如“万几”")
async def got_place_number(place_number: str = ArgPlainText()):
    add_exp = '([\u4e00-\u9fa5])(\d+)'
    query_exp = '([\u4e00-\u9fa5])几'
    if re.fullmatch(add_exp, place_number):
    # 解析输入
        match = re.match(add_exp, place_number)
        if match:
            # 提取机厅名称、人数和当前时间
            hall_name = match.group(1)
            number = match.group(2)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 读取现有的JSON数据或创建新的JSON文件
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {}

            if hall_name in data:
                # 将新数据插入到列表最前面
                data[hall_name].insert(0, {"number": number, "time": current_time})
                # 保留最近的三条数据
                data[hall_name] = data[hall_name][:3]
            else:
                data[hall_name] = [{"number": number, "time": current_time}]
            with open('data.json', 'w') as file:
                json.dump(data, file)

            await guess.finish(f"已成功上报{hall_name}的人数为{number}，上报时间为{current_time}")

    # 如果输入符合查询人数格式
    elif re.fullmatch(query_exp, place_number):
        # 解析输入
        match = re.match(query_exp, place_number)
        if match:
            # 提取机厅名称
            hall_name = match.group(1)

            # 读取JSON数据
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                await guess.finish(f"找不到{hall_name}的人数数据")

            # 查找机厅最近的三条人数数据
            if hall_name in data and len(data[hall_name]) > 0:
                recent_entries = data[hall_name][-3:]
                response = f"{hall_name}最近的三条人数数据为："
                for entry in recent_entries:
                    response += f"\n人数：{entry['number']}，时间：{entry['time']}"
                await guess.finish(response)
            else:
                await guess.finish(f"找不到{hall_name}的人数数据")

    # 如果输入不符合格式
    else:
        await guess.finish(f"输入格式不正确，请按照指定格式输入。")