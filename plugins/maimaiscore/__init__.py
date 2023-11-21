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

guess = on_command("舞萌分数", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)

@guess.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):  
    if args.extract_plain_text():
        matcher.set_arg("level_score", args)


def get_dx_rating_coef(score):
    coef_list = [
        (100.5000, 22.4),
        (100.4999, 22.2),
        (100.0000, 21.6),
        (99.5000, 21.1),
        (99.0000, 20.8),
        (98.0000, 20.3),
        (97.0000, 20.0),
        (94.0000, 16.8),
        (90.0000, 13.6),
        (80.0000, 12.8),
        (75.0000, 12.0),
        (70.0000, 11.2),
        (60.0000, 9.6),
        (50.0000, 8.0),
        (40.0000, 6.4),
        (30.0000, 4.8),
        (20.0000, 3.2),
        (10.0000, 1.6),
        (0.0000, 0.0)
    ]
    for threshold, coef in coef_list:
        if score >= threshold:
            return coef
    else:
        assert(False)

def get_dx_rating(level, score):
    if score >= 100.5000:
        return level * (100.5000 / 100) * get_dx_rating_coef(score)
    return level * (score / 100) * get_dx_rating_coef(score)

def get_comment(score):
    comment_list = [
        (101.0, "我超！101！AP+大神啊！"),
        (100.9, "哇，你一定AP了吧！这个成绩太帅啦！新大神降临~！"),
        (100.5, "这个成绩太帅啦！新大神降临~！"),
        (100.4, "哇，我好崇拜你呀！差一点就鸟加啦！加油~！"),
        (100.0, "哇，我好崇拜你呀！"),
        (99.5, "哇，太厉害啦，下一次一定可以鸟哦~！"),
        (99.0, "好厉害o(≧v≦)o~~~，下一次一定可以鸟哦~！"),
        (98.0, "差一点就到99咯，加油哦~！"),
        (97.0, "差一点就到98咯，加油哦~！"),
        (94.0, "差一点就S咯，加油哦~！"),
        (90.0, "不要越级啦~！建议打一打稍微简单的曲子哦~！"),
        (0, "你看看你打的什么东西！不要越级哦~！建议打一打稍微简单的曲子捏~！")
    ]
    for threshold, comment in comment_list:
        if score >= threshold:
            return comment
    else:
        assert(False)

def score_result(level, score):
    if level > 15:
        return f"捏妈的，你是想打爆舞萌吗？"
    if level < 1:
        return f"捏妈的，华立欠你钱了？"
    if score > 101:
        return f"大于101？你是把滴蜡熊打爆了吗？"
    rating = get_dx_rating(level, score)
    comment = get_comment(score)
    return f"该曲目的分数为 {rating}，{comment}"


@guess.got("level_score", f"请输入定数和分数（中间用空格分开，不加百分号），如“13.4 100.45”")
async def got_level_score(level_score: str = ArgPlainText()):
    reg_exp = "[0-9]+(\\.[0-9])? [0-9]+(\\.[0-9]{1,4})?"
    if not re.fullmatch(reg_exp, level_score):
        await guess.reject(f"输入格式错误，请重新输入")
    level, score = map(float, level_score.split())
    await guess.finish(score_result(level, score))