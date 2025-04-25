"""
该程序只能在本地使用。
"""
import os
import zipfile
import time

from config import path
from config import worldname
from config import backupCount

if worldname == "":
    raise ImportError("没有指定世界")
elif path == "":
    raise ImportError("没有指定服务器目录")
else:
    pass

os.chdir(f"{path}")
#切换到工作目录
if os.path.exists ('backup'):
    pass
else:
    os.mkdir('backup')

def now():
    import time
    # 获取当前时间的时间戳
    current_timestamp = time.time()
    # 将时间戳转换为本地时间
    local_time = time.localtime(current_timestamp)
    # 格式化时间
    formatted_time = time.strftime('%Y-%m-%d %H_%M_%S', local_time)
    return formatted_time

def backup():
    zip_file = str(worldname)
    zip_file_new = zip_file + now() +'.zip'

    # 如果文件存在
    if not os.path.exists(zip_file):
        raise Exception('文件不存在！')
    else:
    # 创建 ZipFile 对象
        with zipfile.ZipFile(zip_file_new, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 写压缩文件
            zipf.write(zip_file)
        print('文件压缩成功！')


while True:
    backup()
    time.sleep(backupCount)