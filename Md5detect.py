# 根据MD5计算文件夹内重复文件,并输出

import os
import hashlib

def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

def find_duplicate_files(folder_path):
    hash_dict = {}
    duplicates = []

    filenames = os.listdir(folder_path)
    for index, filename in enumerate(filenames):
        file_path = os.path.join(folder_path, filename)
        file_hash = calculate_md5(file_path)
        # 打印当前index
        print('\r', f"当前处理文件：{index + 1}/{len(filenames)}",end="")

        if file_hash in hash_dict:
            duplicates.append((hash_dict[file_hash], file_path))
        else:
            hash_dict[file_hash] = file_path

    return duplicates

folder_path = "your_folder_path"
duplicate_files = find_duplicate_files(folder_path)

if duplicate_files:
    print("重复文件:")
    for duplicate in duplicate_files:
        print(f"{duplicate[0]} 与 {duplicate[1]}")
else:
    print("没有重复文件。")