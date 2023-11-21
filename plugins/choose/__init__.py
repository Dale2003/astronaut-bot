import os
import random
import wave
import contextlib
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.permission import GROUP_MEMBER,PRIVATE,GROUP
from nonebot.matcher import Matcher

import re

guess = on_command("帮我选", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)

@guess.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):  
    if args.extract_plain_text():
        matcher.set_arg("choice", args)


@guess.got("choice", f"请输入要选择的内容（中间用空格分开）")
async def got_choice(choice: str = ArgPlainText()):
    choice_list = choice.split(" ")
    if len(choice_list) == 1:
        await guess.finish("只有一个选项，不用选了吧")
    else:
        choice_list += ["。。。嘿，您猜怎么着，我都不选！", "。。。小孩子才做选择，我都要！"]
        await guess.finish(f"我选{random.choice(choice_list)}")