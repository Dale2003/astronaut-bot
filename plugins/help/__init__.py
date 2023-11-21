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

def help():
    res = "pku区：\n    吃什么\n    去哪自习\n    去哪睡觉\n    去哪玩\n    信科教务（信科强基、强基）\n游戏区：\n    wordle（加-l 数字指定长度）\n    成语wordle（猜成语、handle（需要at））\n    扫雷（需要at）\n    人生重开（remake/liferestart/人生重来）（需要at）\n整活区：\n    语句抽象化（抽象 [要抽象的语句]）\n    发病语录（发病+名字）\n    关键词+@成员触发表情包制作\n    pjsk表情制作(pjsk)\n    猫猫虫图片发送(capoo)\n    舔狗日记\n    自动对对联（对联+上联）\n    emojimix（emoji+emoji）\n    词云（今日词云）\n    疯狂星期x\n    今日老婆\n    /群话痨排行榜\n    骂人的话+@我\n音游区：\n    猜曲绘\n    猜歌曲 （仅限phigros）\n    去哪出勤（去哪打mai）\n    maimai机器人"
    return res

guess = on_command("help", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)
pic = MessageSegment.image('file:///D:/BaiyuBot/first_bot/first_bot/plugins/help/pic.png')

@guess.handle()
async def handle_function():
    global res
    res = help()
    await guess.send(pic)