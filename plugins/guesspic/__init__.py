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

selected_image_file = {}
cropped_pic1 = {}
cropped_pic2 = {}
cropped_pic3 = {}
cropped_pic4 = {}
raw_pic = {}
song_name = {}
is_playing = {}

with open('D:/BaiyuBot/first_bot/first_bot/plugins/maimaiDX/static/all_alias.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

def random_pic(id_group,choice):
    if (choice == "pgr"):
        image_folder = 'D:/phigros曲绘（部分别名版）'
        image_files = [f for f in os.listdir(image_folder) if  f.endswith('.png')]
        selected_image_file[id_group] = random.choice(image_files)
        image_path = os.path.join(image_folder, selected_image_file[id_group])
        width1 = 400
        height1 = 400
        width2 = 300
        height2 = 300
        width3 = 200
        height3 = 200
        width4 = 100
        height4 = 100
    else:
        random_song_id, random_song_data = random.choice(list(data.items()))
        image_folder = 'D:/BaiyuBot/first_bot/first_bot/plugins/maimaiDX/static/mai/cover'
        image_files = [f for f in os.listdir(image_folder) if  f.endswith('.png')]
        selected_image_file[id_group] = random_song_id+".png"
        image_path = os.path.join(image_folder, selected_image_file[id_group])
        width1 = 200
        height1 = 200
        width2 = 160
        height2 = 160
        width3 = 110
        height3 = 110
        width4 = 70
        height4 = 70

    image = Image.open(image_path)
    width, height = image.size
    x = random.randint(0, width-width2)
    y = random.randint(0, height-height2)
    box = (x, y, x+width2, y+height2)
    cropped_image = image.crop(box)
    cropped_image = cropped_image.convert('L')
    cropped_image.save("D:/dale/save_image/cropped_image2_"+id_group+".png", quality=50)

    x = random.randint(0, width-width3)
    y = random.randint(0, height-height3)
    box = (x, y, x+width3, y+height3)
    cropped_image = image.crop(box)
    cropped_image = cropped_image.convert('L')
    cropped_image.save("D:/dale/save_image/cropped_image3_"+id_group+".png", quality=50)

    x = random.randint(0, width-width4)
    y = random.randint(0, height-height4)
    box = (x, y, x+width4, y+height4)
    cropped_image = image.crop(box)
    cropped_image = cropped_image.convert('L')
    cropped_image.save("D:/dale/save_image/cropped_image4_"+id_group+".png", quality=50)

    x = random.randint(0, width-width1)
    y = random.randint(0, height-height1)
    box = (x, y, x+width1, y+height1)
    cropped_image = image.crop(box)
    cropped_image.save("D:/dale/save_image/cropped_image1_"+id_group+".png", quality=50)

    image.save("D:/dale/save_image/image_"+id_group+".png", quality=50)
    
    cropped_pic1[id_group] = MessageSegment.image('file:///D:/dale/save_image/cropped_image1_'+id_group+'.png')
    cropped_pic2[id_group] = MessageSegment.image('file:///D:/dale/save_image/cropped_image2_'+id_group+'.png')
    cropped_pic3[id_group] = MessageSegment.image('file:///D:/dale/save_image/cropped_image3_'+id_group+'.png')
    cropped_pic4[id_group] = MessageSegment.image('file:///D:/dale/save_image/cropped_image4_'+id_group+'.png')

    raw_pic[id_group] = MessageSegment.image('file:///D:/dale/save_image/image_'+id_group+'.png')
    if choice == "pgr":
        song_name[id_group]=selected_image_file[id_group].split("_")[1].split(".")[0]
    else:
        song_name[id_group]=random_song_id
    return cropped_pic1[id_group], cropped_pic2[id_group],cropped_pic3[id_group],cropped_pic4[id_group], raw_pic[id_group], song_name[id_group]

def game_running(event: GroupMessageEvent) -> bool:
    gid = str(event.group_id)
    return is_playing.get(gid, False)

guess = on_command("猜曲绘", block=True, priority=13)
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
    random_pic(gid,choice[gid])
    if (choice[gid] == "mai"):
        await guess.send(f"请选择难度（1为简单，2为中等，3为困难，4为地狱）")
    elif (choice[gid] == "pgr"):
        await guess.send(f"请选择难度（1为简单，2为中等，3为困难，4为地狱）")
    else:
        await guess.reject(f"请选择mai或pgr")

@guess.got("sel")
async def got_sel(event: GroupMessageEvent, sel: str = ArgPlainText()):
    gid = str(event.group_id)
    if (sel == "1"):
        await guess.send(f"请输入曲目名称\n"+cropped_pic1[gid]+"输入“不玩了”退出游戏")
        is_playing[gid] = True
    elif (sel == "2"):
        await guess.send(f"请输入曲目名称\n"+cropped_pic2[gid]+"输入“不玩了”退出游戏")
        is_playing[gid] = True
    elif (sel == "3"):
        await guess.send(f"请输入曲目名称\n"+cropped_pic3[gid]+"输入“不玩了”退出游戏")
        is_playing[gid] = True
    elif (sel == "4"):
        await guess.send(f"请输入曲目名称\n"+cropped_pic4[gid]+"输入“不玩了”退出游戏")
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
            await guess.finish(f"游戏结束，正确答案是"+song_name[gid]+"\n"+raw_pic[gid])
            await handle.finish()
            return
        else:
            song_data = data[song_name[gid]]
            is_playing[gid] = False
            await guess.finish(f"游戏结束，正确答案是"+song_name[gid]+":"+song_data['Name']+"\n"+raw_pic[gid])
            await handle.finish()
            return
    else:
        if choice[gid] == "pgr":
            if (ans.lower() in song_name[gid].lower()) and (ans != ""):
                is_playing[gid] = False
                await guess.finish(f"恭喜你答对了，正确答案是"+song_name[gid]+"\n"+raw_pic[gid], at_sender=True)
                await handle.finish()
                return
        else:
            song_data = data[song_name[gid]]
            if (ans.lower() == song_data['Name']) or ans.lower() in song_data['Alias'] and (ans != ""):
                is_playing[gid] = False
                await guess.finish(f"恭喜你答对了，正确答案是"+song_name[gid]+":"+song_data['Name']+"\n"+raw_pic[gid], at_sender=True)
                await handle.finish()
                return
