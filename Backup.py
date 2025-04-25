"""
该程序只能在本地使用。
只需要将此文件和config复制到同一目录即可工作。
"""
import os
import tarfile
import time

from config import path
from config import world
from config import backupCount

if world == "":
    raise ImportError("没有指定世界")
elif path == "":
    raise ImportError("没有指定服务器目录")
else:
    pass

os.chdir(f"{path}")
#切换到工作目录
# if os.path.exists ('backup'):
#     pass
# else:
#     os.mkdir('backup')

def now(): #用于获取当前时间，并转换为可读的方式
    import time
    # 获取当前时间的时间戳
    current_timestamp = time.time()
    # 将时间戳转换为本地时间
    local_time = time.localtime(current_timestamp)
    # 格式化时间
    formatted_time = time.strftime('%Y-%m-%d %H_%M_%S', local_time)
    return formatted_time

def tar_create(output_filename,source_dir,compression="w:gz"):
    with tarfile.open(output_filename,compression) as tar:
        tar.add(source_dir,arcname=os.path.basename(source_dir))

while True:

    if not os.path.exists(world):
        raise Exception('目录不存在！')

    clock = str(now())
    tar_name = f"Backup_{clock}.tar.gz"
    tar_create(tar_name,world)
    print(f"成功创建归档：Backup_{clock}.tar.gz")

    time.sleep(backupCount) #在config中可以设置备份时长。