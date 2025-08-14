from moviepy.editor import VideoFileClip
origin_video = "I:/迅雷下载/try/origin/ori_8_1.mp4"
des_audo = "I:/迅雷下载/try/code_process/8_1.wav"

if __name__ == "__main__":
    print ("start process video {}".format(origin_video))
    video = VideoFileClip(origin_video)
    print ("start write audo {}".format(des_audo))
    video.audio.write_audiofile(des_audo)
