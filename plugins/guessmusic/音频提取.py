import os
import shutil

# 指定目标文件夹路径
source_directory = 'D:/Output_NoBGA_FesPlus/東方Project'
destination_directory = 'D:\dale\maisong'

def extract_and_rename_mp3_files(source_dir, dest_dir):
    # 获取目标文件夹下所有文件夹的名字
    folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]

    for folder in folders:
        folder_path = os.path.join(source_dir, folder)
        # 检查文件夹中是否存在track.mp3文件
        mp3_file = os.path.join(folder_path, 'track.mp3')

        if os.path.exists(mp3_file):
            # 解析数字id
            folder_id = folder.split('_')[0]

            # 重命名track.mp3文件
            new_filename = folder_id + '.mp3'
            new_file_path = os.path.join(dest_dir, new_filename)

            # 如果新文件名已存在，则加上序号避免重复
            count = 1
            while os.path.exists(new_file_path):
                new_filename = folder_id + '_' + str(count) + '.mp3'
                new_file_path = os.path.join(dest_dir, new_filename)
                count += 1

            # 将文件移动到指定目录
            shutil.move(mp3_file, new_file_path)
            print(f"Moved {mp3_file} to {new_file_path}")

# 执行函数
extract_and_rename_mp3_files(source_directory, destination_directory)
