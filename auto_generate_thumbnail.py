import subprocess
import os
from tqdm import tqdm
from datetime import datetime
import hashlib

def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

def extract_frames(video_path, extract_folder, total_frames, tile):
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    frame_num = int(tile.split('x')[0]) * int(tile.split('x')[1])

    frame_interval = max(total_frames // frame_num, 1)  # Ensure at least one frame is selected
    output_pattern = os.path.join(extract_folder, 'frame_%04d.png')

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'select=not(mod(n\\,{frame_interval}))',
        '-vsync', 'vfr',
        output_pattern,
        '-y'
    ]

    subprocess.run(cmd,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_thumbnail_grid(input_folder, output_path, thumbnail_size, tile):
    cmd = [
        'ffmpeg',
        '-pattern_type', 'glob',
        '-i', os.path.join(input_folder, 'frame_*.png'),
        '-filter_complex', f'scale={thumbnail_size[0]}:{thumbnail_size[1]},tile={tile}',
        output_path,
        '-y'
    ]

    subprocess.run(cmd,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_thumbnail(video_folder, output_folder, thumbnail_size, tile):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 新建log.txt
    with open(log_path, "w") as file:
        file.write(f"Start,{datetime.now()}\n")

    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith((".mp4", ".wmv", ".avi", ".mkv", ".mov"))]
    for video_file in tqdm(video_files, desc="Processing Videos", unit="video"):
        try:
            video_path = os.path.join(video_folder, video_file)
            output_path = os.path.join(output_folder, video_file.split('.')[0] + ".jpg")

            file_hash = calculate_md5(video_path)
            # 如果当前hash存在,则写入记录,直接结束本层循环,不生成缩略图
            if file_hash in hash_dict:
                with open(log_path, "a") as file:
                    file.write(f"Duplicates,{video_path} 与 {hash_dict[file_hash]}\n")
                continue
            else:
                hash_dict[file_hash] = video_path

            total_frames_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames', '-of', 'default=nokey=1:noprint_wrappers=1', video_path]
            total_frames = int(subprocess.check_output(total_frames_cmd).decode('utf-8').strip())

            extract_frames(video_path, output_folder+'/_extract_folder', total_frames, tile)
            create_thumbnail_grid(output_folder+'/_extract_folder', output_path, thumbnail_size, tile)
            
            #追加写入当前成功记录
            with open(log_path, "a") as file:
                file.write(f"Success,{video_path}\n")

        except Exception as e:
            #在开头插入失败记录
            with open(log_path, "r") as file:
                content = file.readlines()    # 读取文件的所有行
            content.insert(1, f'Error,{video_path}\n')    # 在指定位置插入新行
            with open(log_path, "w") as file:
                file.writelines(content)    # 将更新后的内容写入文件

            print(f"生成缩略图错误:{video_path}, {e}")
    
    # 缩略图生成完成
    print('缩略图生成完成。')
    with open(log_path, "a") as file:
        #写入当前时间
        file.write(f"FINISH,{datetime.now()}\n")

# 通用设置
hash_dict = {}  #存hash dict init
duplicates = [] #存重复文件名
thumbnail_width = 90    #单帧宽度
thumbnail_height = 160  #单帧高度
thumbnail_size_times = 12   #取单帧像素倍数
thumbnail_size=(thumbnail_width*thumbnail_size_times, thumbnail_height*thumbnail_size_times)
tile = '4x4'    # 缩略图排列模式,中间请用x链接,程序自动解析模式与需要取的帧数

# 示例用法：
video_folder = 'your_video_folder_path' #处理的文件夹路径
output_folder = 'your_output_folder_path'   #输出文件夹路径, 可以与输入一致, 默认输出文件与源文件同名
log_path = output_folder + '/_log.txt'  #输出log路径
create_thumbnail(video_folder, output_folder, thumbnail_size, tile)
