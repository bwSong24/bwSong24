import subprocess
import time 
import os
import sys 
import logging

sys.path.append("../common_pkg/")

# 包 LogForPy 在git 上的common_pkg 中维护
from LogForPy.emb_log import config_logging

config_logging("./log/transcode.log")

origin_file = "I:/迅雷下载/tan_tu_orgin/RPReplay_Final1701577757.MP4"
origin_file = "I:/迅雷下载/tan_tu_orgin/20230225_5.MP4"
# 目录模式
origin_dir = "I:/迅雷下载/prepair_use_ffmpeg/origin/"
des_dir = "I:/迅雷下载/prepair_use_ffmpeg/result/"

# 这个啥都没变，就是改一下格式，比如把 mp4改成 mkv
cmd = "ffmpeg -i {} -c:v copy -c:a copy {}".format(origin_file, des_file)


# 我再尝试下，尺寸自动变化的，这个时间更短，变成8分钟了，-1那个地方其实是512，靠它自己计算  
# general_cmd = "ffmpeg -i {} -vf scale=-1:1080 -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {}".format(origin_file, des_file)

# 我把分辨率和视频显示，这两个结合起来试一下,再加个 aspect 呢，感觉有戏啊，草死它啊，竟然成了，花了也就11分钟的时间  
# 其实分辨率 -s 和 视频显示 -vf的任意一种结合 aspect，都可以实现人形不被拉长
general_cmd = "ffmpeg -i {} -s 888x1080 -vf scale=510:1080 -aspect 0.462  -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {} -y".format(origin_file, des_file)
# 要不我把 scale 去掉再试试呢，也是可以实现的，大小多了20M，这不算啥，时间12min  
# general_cmd = "ffmpeg -i {} -s 888x1080  -aspect 510:1080  -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {}".format(origin_file, des_file)

if __name__ == "__main__":
    cmd = general_cmd
    print ("start run command: {}".format(cmd))
    trans_start_time = time.time()
    subprocess.run(cmd)#返回‘0’就说明合并成功了
    trans_end_time = time.time()
    spend_time = trans_end_time - trans_start_time

    print ("run end.[{}]".format(spend_time))

    # # 下面这是目录模式
    # origin_files = [file for file in os.listdir(origin_dir)]
    # for file in origin_files:  
    #     origin_file = origin_dir + file 
    #     des_file = des_dir + file 
    #     cmd = "ffmpeg -i {} -s 888x1080 -vf scale=510:1080 -aspect 0.462  -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {} -y".format(origin_file, des_file)
    #     logging.debug ("start run command: {}".format(cmd) )
    #     trans_start_time = time.time()
    #     subprocess.run(cmd)#返回‘0’就说明合并成功了
    #     trans_end_time = time.time()
    #     spend_time = (trans_end_time - trans_start_time)/60
    #     logging.debug ("run end.[{}]".format(spend_time))

    

    
    