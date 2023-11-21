from pydub import AudioSegment
import os

# 指定目标文件夹路径
source_directory = 'D:/dale/maisong'

def mp3_to_wav(source_dir):
    # 遍历目标文件夹下所有文件
    for filename in os.listdir(source_dir):
        if filename.endswith(".mp3"):
            mp3_file = os.path.join(source_dir, filename)
            # 读取mp3文件
            sound = AudioSegment.from_mp3(mp3_file)
            # 提取文件名（不含扩展名）
            file_name, _ = os.path.splitext(filename)
            # 定义输出的wav文件路径和文件名
            wav_file = os.path.join(source_dir, f"{file_name}.wav")
            # 导出wav文件
            sound.export(wav_file, format="wav")
            print(f"Converted {mp3_file} to {wav_file}")

# 执行函数
mp3_to_wav(source_directory)
