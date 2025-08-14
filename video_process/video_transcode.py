import cv2
import time 
import sys  
import logging

sys.path.append("../common_pkg/")

# 包 LogForPy 在common_pkg 中维护
from LogForPy.emb_log import config_logging

config_logging("./log/process_video.log")
 
# VideoCapture方法是cv2库提供的读取视频方法
# 此视频 873M, 时长是1h10min4s  
cap = cv2.VideoCapture('I:/迅雷下载/try/origin/ori_8_1.mp4')
# 设置需要保存视频的格式 "XVID"，该参数是MPEG-4编码类型，文件名后缀为.avi
# 若设置需要保存视频的格式 "MP4V"，则文件的后缀名是.mp4   
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 视频编解码器
# 设置视频帧频
fps = cap.get(cv2.CAP_PROP_FPS)
# 设置视频大小
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# VideoWriter方法是cv2库提供的保存视频方法
# 按照设置的格式来out输出，这里如果手动改变fps，视频的时长就和原视频时长不一样，在合并音视频时，不好合并
# 按照 fps不变，生成的视频的大小是 1.49G
out = cv2.VideoWriter('I:/迅雷下载/try/code_process/8_1.avi',fourcc ,fps, size)
# 这里我手动改变fps 为23, 时长变成了 1h31min24s
# fps = 23
# out = cv2.VideoWriter('I:/迅雷下载/try/code_process/8_1_try_speed.mp4', fourcc, fps, size)  # 写入视频
 
# 确定视频打开并循环读取
fram_num = 0
save_path = "I:/pictures"
write_start_time = time.time()
while(cap.isOpened()):
    # 逐帧读取，ret返回布尔值
    # 参数ret为True 或者False,代表有没有读取到图片
    # frame表示截取到一帧的图片
    ret, frame = cap.read()
    if ret == True:
        # 垂直翻转矩阵
        # frame = cv2.flip(frame,0)
 
        out.write(frame)
 
        # cv2.imshow('frame',frame)
        logging.debug ("{}th frame".format(fram_num))
        fram_num = fram_num + 1
        if fram_num % 15000 == 0:
            # cv2.imshow('frame',frame)
            logging.debug ("save {}th picture".format(fram_num))
            cv2.imwrite(save_path + "/"+ str(fram_num)+".jpg",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.debug ("waitKey")
            break
    else:
        logging.debug ("No image was read")
        break

write_end_time = time.time()
logging.debug ("Total time taken to turn video: {}".format(write_end_time - write_start_time)) 

# 释放资源
cap.release()
out.release()
# 关闭窗口
cv2.destroyAllWindows()