&emsp;&emsp;这是一些关于视频转码的代码，之所以考虑视频转码，是因为国内某盘，很正常的视频，你传到某盘上就会被列为违规视频，曾经我也考虑过国外网盘，还是觉着麻烦，也查过一些资料，有说打成压缩包，再进行加密的，但这样就不能观看了，还记得在早些年，我尝试过一种方法，就是下载时，下载到99%，赶紧停止，这样，既不会被列为违规视频，播放器也能够播放，但这个火候太难把握了，一不留神就 100%了，这才考虑到了转码     
&emsp;&emsp;一转码，文件的md5值就发生了改变，理论上就检测不到了，当然如果它采用更先进的手段，抽取某一帧，利用图像识别，那转码估计也不好使，但这样是不就侵犯隐私了啊        

&emsp;&emsp;后来又有个需求，我发现我那么大的手机空间怎么没怎么用，就快满了，后来发现，我录屏一个视频，四五十分钟的都得好几个G，再加之，视频转码或许也是一门技术，不如就研究一下
&emsp;&emsp;我整个的一个探索过程分成3个阶段，第一阶段是用 python 程序处理，首先用 python 把视频重读了一下，转换成另外一种格式的视频，但我发现没有声音，所以用 python 程序处理，分成两部分，一部分处理视频，一部分提取音频，然后音视频一合并就可以了，但是用 python 程序处理好像有两个问题，一个是如果改变视频帧率，视频时长会变，这样在音视频合并的时候就不同步了，另外一个是，用 python 转视频，似乎不支持转变码率，这样转出来的视频会很大，这也并不是我想要的，当然或许是我研究的还不够深入，由此进入了第二个阶段，寻找一些软件帮我做这件事情       
&emsp;&emsp;第二个阶段，我找到了两个工具，一个是 HandBrake，专门用于视频转码的，真挺好用的，文章[HandBrake 使用](https://www.bilibili.com/opus/398176492345677149)，关于如何使用 HandBrake，讲的特别清楚，一个是 MediaInfo，是用来帮我查看视频的信息的，比如码率、帧率、尺寸都具体信息都有，也很方便，但如果视频多的话，我还得一个视频一个视频的手动点击处理，没有用程序方便啊，后来了解到 HandBrake的底层是用的 ffmpeg，开始第三个阶段，研究 ffmpeg         
&emsp;&emsp;ffmpeg 确实是强大，对于 ffmpeg的研究，也只是让我熟悉了一些参数而已，其它倒没有啥了    


* video_transcode.py  
&emsp;&emsp;此文件是利用python的cv2库对视频进行转码，在代码中，原视频 "I:/迅雷下载/try/origin/ori_8_1.mp4" ，大小 873M, 时长是1h10min4s，在fps不变，也就是帧率不变的情况下，转出来的avi视频，大小是1.49G，时长不变，耗时40min，当然如果 fps发生改变，文件的大小或许可以控制，但时长也会发生改变，这将会对音视频的合并造成困难    
* extract_audo.py  
&emsp;&emsp;此文件是用来提取音频的，这个很快  
* merge_video_audeo.py  
&emsp;&emsp;此文件是把前两个文件得出的视频和音频进行合并，本质用的还是 ffmpeg，速度也很快  

关于整个探索过程，我在 csdn的文章上也有记录，地址 https://blog.csdn.net/weileshenghuo1/article/details/144793084?spm=1001.2014.3001.5502  

关于如何使用 ffmpeg，也就是可执行文件 use_ffmpeg.py，我把这些尝试记录在这里  
* 高效命令，含有 "ultra" 的变量   
&emsp;&emsp;这类命令，有它自己的优势，压缩比很高，7.5G 的视频可以压缩到300M，但弱点也明显，一是耗时时间太长，二是无法导入苹果相册，还是算了吧，具体尝试如下：   
```
# 原 7.5G 的视频，用它可以生成  285M的mkv 视频，当然截取了30s，耗时都将近一个半小时 
ori_ultra_cmd = "ffmpeg -hide_banner -hwaccel auto -ss 30 -i {} -vcodec hevc -preset slow -b:v 891k -acodec aac -aac_coder twoloop -b:a 102k {} -y ".format(
    origin_file, des_file)
# -ss 30 其实是视频裁剪，从30s开始裁剪，所以去掉 -ss 30，另外对音频那里要求也不高，所以把音频部分以去掉了，耗时仍然很长，一个半小时
ultra_cmd = "ffmpeg -hide_banner -hwaccel auto -i {} -vcodec hevc -preset slow -b:v 891k -r 30 {} -y ".format(
    origin_file, des_file)
# 只改变码率和帧率，果真时间缩短到了17分钟，但也有弊端，你不知道码率和帧率应该是多少
simple_ultra_cmd = "ffmpeg -i {} -b:v 891k -r 30 {} -y ".format(
    origin_file, des_file)
```
* 次高效命令，命令中有 "general" 的命令  
&emsp;&emsp;主要是通过改变分辨率改变视频的大小，如果改变分辨率，视频中的人就会变形，最终通过 aspect参数解决，视频的大小和转换时长都可接受，当然也是经过了一些尝试，现在是7.5G的视频可以转换到500M左右，耗时15min以内，所以目前可用，一开始的原始命令是 ffmpeg -i input.mp4 -c:v libx264 -preset slow  -qp 22 -c:a copy output.mp4，出自文章[工具 ffmpeg](https://blog.csdn.net/qq_46106285/article/details/130340049)
，具体的尝试如下：  
 * 原 7.5G 的视频，用它可以生成了  883M的mp4 视频，耗时大概35min 左右，此时 preset 的参数是 slow   
 * 我把 preset 的参数改成 medium ,时间变短了，26min，但空间竟然变成了908M   
 * 我把参数改成 fast ,时间虽然变成了19min，但文件大小并没有变小啊，是 909M  
 * 把 qp 变成 crf ,大小确实小了点，变成 730M  
 * 我再加个帧率，把帧率变成 30，大小几乎没有变化啊  

&emsp;&emsp;后来我发现，HandBrake 可以把视频转到500M，为啥，我只能转到730呢？经对比发现是分辨率问题，所以开始着手修改分辨率，显示使用 -vf scale=888:1080，发现整个画面比例都变了，人变宽了，然后我把 -vf 参数，换成 -s 888x1080 试完之后，效果是一样的，还是人变宽了   
&emsp;&emsp;再后来找到一篇文章，把宽的部分填充成黑色，大小直接压缩到了 285M,真是牛逼啊，时间也短了，10分钟左右，但有个问题，放在手机上，还是有黑框，这样看视频的观感也不行啊，命令如下：  
```
general_cmd = 'ffmpeg -i {} -vf "scale=512:1080,pad=888:1080:(iw+ow)/2:0:black" -aspect 888:1080 -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {}'.format(origin_file, des_file)
```  
&emsp;&emsp;这里其实要明白一个东西，原视频的分辨率，按照等比缩放，是刚好缩放到 512:1080，但我是觉着这样的分辨率过低，所以强行将 512改成了888，这样分辨率就高了，但人的比例也就拉长了，其实我只要不强行改变分辨率的比例，就按原始的比例，如下命令，参数都可以写死，很方便的  
```
# general_cmd = "ffmpeg -i {} -vf scale=-1:1080 -c:v libx264 -preset fast  -crf 22 -r 30 -c:a copy {}".format(origin_file, des_file)
```
&emsp;&emsp; 使用 x265 尝试了下，发现手机无法播放 -c:v libx265   
&emsp;&emsp;那么问题来了，我就是想让分辨率是 888x1080，但人又不被拉长，可以吗？当时我陷入了执拗，不过还好解决了，最后加上了 aspect 参数解决了  