#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/5 1:49
# @Author  : 剑客阿良_ALiang
# @Site    : 
# @File    : video_add_audio_tool.py
 
import os
import uuid
from ffmpy import FFmpeg
 
 
# 视频添加音频
def video_add_audio(video_path: str, audio_path: str, output_dir: str):
    _ext_video = os.path.basename(video_path).strip().split('.')[-1]
    _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
    if _ext_audio not in ['mp3', 'wav']:
        raise Exception('audio format not support')
    _codec = 'copy'
    if _ext_audio == 'wav':
        _codec = 'aac'
    result = os.path.join(
        output_dir, '{}.{}'.format(
            uuid.uuid4(), _ext_video))
    ff = FFmpeg(
        inputs={video_path: None, audio_path: None},
        outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -shortest'.format(_codec)})
    print(ff.cmd)
    ff.run()
    return result

if __name__ == '__main__':
    extra_audeo = "I:/迅雷下载/try/code_process/8_1.wav"
    video_without_souund = "I:/迅雷下载/try/code_process/8_1.avi"
    des_dir = "I:/迅雷下载/try/code_process/"
    video_add_audio(video_without_souund, extra_audeo, des_dir)