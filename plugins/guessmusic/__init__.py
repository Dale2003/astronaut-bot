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
import os
import random
from PIL import Image
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import on_command, on_message, logger
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.rule import to_me, Rule
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent, ActionFailed, Message
from nonebot.adapters.onebot.v11.permission import GROUP_MEMBER,PRIVATE,GROUP
from nonebot.matcher import Matcher
import json
import random
from PIL import Image

is_playing = {}
music1 = {}
music2 = {}
selected_music = {}
song_name = {}
out_file1 = {}
out_file2 = {}
selected_music_file = {}
choice = {}
data = {}

with open('D:/BaiyuBot/first_bot/first_bot/plugins/maimaiDX/static/all_alias.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

def random_music(id_group,choice,data):
    
    # 指定音乐文件所在的文件夹路径
    if (choice == "pgr"):
        music_dir = "D:\phigros原声带（已命名）"

        # 获取音乐文件列表
        music_list = [f for f in os.listdir(music_dir) if f.endswith('.wav')]
        # 从列表中随机选取一首音乐文件
        selected_music_file[id_group] = random.choice(music_list)
        # 打开选中的音乐文件
        music_path = os.path.join(music_dir, selected_music_file[id_group])
    
    else:
        random_song_id, random_song_data = random.choice(list(data.items()))
        music_dir ="D:\dale\maisong"

        # 获取音乐文件列表
        music_list = [f for f in os.listdir(music_dir) if f.endswith('.wav')]
        # 从列表中随机选取一首音乐文件
        selected_music_file[id_group] = random_song_id+".wav"
        # 打开选中的音乐文件
        music_path = os.path.join(music_dir, selected_music_file[id_group])

    # 简单（6秒）
    with contextlib.closing(wave.open(music_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        
        # 随机选取6秒片段起始时间
        start = random.uniform(0, duration - (6))
        
        # 按片段长度读取音乐文件数据
        f.setpos(int(start * rate))
        data = f.readframes(int(6* rate))
    # 保存音乐片段
    out_file1[id_group] = "D:/dale/save_wav/selected_segment1"+ id_group +".wav"
    with wave.open(out_file1[id_group], "w") as out_f:
        out_f.setnchannels(f.getnchannels())
        out_f.setsampwidth(f.getsampwidth())
        out_f.setframerate(rate)
        out_f.writeframes(data)

    # 难（3秒）
    with contextlib.closing(wave.open(music_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        
        # 随机选取5秒片段起始时间
        start = random.uniform(0, duration - (3))
        
        # 按片段长度读取音乐文件数据
        f.setpos(int(start * rate))
        data = f.readframes(int(3* rate))
    
    # 保存音乐片段
    out_file2[id_group] = "D:/dale/save_wav/selected_segment2"+ id_group +".wav"
    with wave.open(out_file2[id_group], "w") as out_f:
        out_f.setnchannels(f.getnchannels())
        out_f.setsampwidth(f.getsampwidth())
        out_f.setframerate(rate)
        out_f.writeframes(data)

    if (choice == "pgr"):
        # 获取音乐文件名
        selected_music[id_group]=selected_music_file[id_group].split("_")[1].split(".")[0]
        song_name[id_group]=selected_music[id_group]
    else:
        # 获取音乐文件名
        selected_music[id_group]=selected_music_file[id_group].split(".")[0]
        song_name[id_group]=selected_music[id_group]

    music1[id_group] = MessageSegment.record(file = 'file:///D:/dale/save_wav/selected_segment1'+id_group+'.wav', magic = 0)
    music2[id_group] = MessageSegment.record(file = 'file:///D:/dale/save_wav/selected_segment2'+id_group+'.wav', magic = 0)

    return

def game_running(event: GroupMessageEvent) -> bool:
    gid = str(event.group_id)
    return is_playing.get(gid, False)

guess = on_command("猜歌曲", block=True, priority=13)
# guess = on_command("猜曲绘", block=True, permission=GROUP_MEMBER|PRIVATE|GROUP)

choice = {}

@guess.handle()
async def handle_function(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    gid = str(event.group_id)
    if (game_running(event)):
        await guess.finish(f"游戏正在进行中，请先结束游戏")
        return
    if args.extract_plain_text():
        matcher.set_arg("choi", args)


@guess.got("choi", f"请选择题库（mai/pgr)")
async def got_choice(event: GroupMessageEvent, choi: str = ArgPlainText()):
    gid = str(event.group_id)
    if (game_running(event)):
        await guess.finish(f"游戏正在进行中，请先结束游戏")
        return
    choice[gid] = choi
    random_music(gid,choice[gid],data)
    if (choice[gid] == "mai"):
        await guess.send(f"请选择难度（1为简单，2为困难）")
    elif (choice[gid] == "pgr"):
        await guess.send(f"请选择难度（1为简单，2为困难）")
    else:
        await guess.reject(f"请选择mai或pgr")

@guess.got("sel")
async def got_sel(event: GroupMessageEvent, sel: str = ArgPlainText()):
    gid = str(event.group_id)
    if (sel == "1"):
        await guess.send(f"请输入曲目名称\n"+"输入“不玩了”退出游戏")
        await guess.send(music1[gid])
        is_playing[gid] = True
    elif (sel == "2"):
        await guess.send(f"请输入曲目名称\n"+"输入“不玩了”退出游戏")
        await guess.send(music2[gid])
        is_playing[gid] = True
    else:
        await guess.reject(f"输入错误，请重新输入")

handle = on_message(Rule(game_running),block=False, priority=12)
@handle.handle()
async def got_ans(event: GroupMessageEvent):
    gid = str(event.group_id)
    ans = str(event.get_message())
    uid = str(event.user_id)
    if (ans == "不玩了"):
        if choice[gid] == "pgr":
            is_playing[gid] = False
            await guess.finish(f"游戏结束，正确答案是"+song_name[gid])
            await handle.finish()
            return
        else:
            song_data = data[song_name[gid]]
            is_playing[gid] = False
            await guess.finish(f"游戏结束，正确答案是"+song_name[gid]+":"+song_data['Name'])
            await handle.finish()
            return
    else:
        if choice[gid] == "pgr":
            if (ans.lower() in song_name[gid].lower()) and (ans != ""):
                is_playing[gid] = False
                await guess.finish(f"恭喜你答对了，正确答案是"+song_name[gid], at_sender=True)
                await handle.finish()
                return
        else:
            song_data = data[song_name[gid]]
            if (ans.lower() == song_data['Name']) or ans.lower() in song_data['Alias'] and (ans != ""):
                is_playing[gid] = False
                await guess.finish(f"恭喜你答对了，正确答案是"+song_name[gid]+":"+song_data['Name'], at_sender=True)
                await handle.finish()
                return