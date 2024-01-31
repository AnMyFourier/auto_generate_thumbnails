# 得到文件夹内文件种类,并分别统计个数

import os
import glob
from collections import Counter

def count_file_types(folder_path):
    # 使用 glob 获取文件夹下所有文件的路径
    files = glob.glob(os.path.join(folder_path, '*'))
    
    # 提取文件类型
    file_types = [os.path.splitext(file)[1].lower() for file in files if os.path.isfile(file)]
    
    # 使用 Counter 统计每种文件类型的个数
    file_type_counter = Counter(file_types)

    return file_type_counter

# 替换 'your_folder_path' 为目标文件夹的路径
folder_path = 'your_folder_path'
file_type_counts = count_file_types(folder_path)

print("文件类型及其个数:")
for file_type, count in file_type_counts.items():
    print(f"{file_type}: {count} 个")
