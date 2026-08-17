这是一个基础的通过 expect 登录相应 shell 的脚本(它是通过本地的shell 就可以用，不需要借助item 的profile)     

当然它还有另外一种使用方式，就是放在 item 的 profile 中，你可以看到我的 profile 中有类似：  

```
/Users/songbw/auto_login/core.ex 10.100.19.173 22 yanfa buYvjYDSzYGG5r
```

这种就是我直接利用了 item 的 profile，也比较方便，其实我后来大多都改成了这种方式，我早期用的是，读取文件 computerInfo.ini ，并列出登录机器的方式，只能说各有各的好处吧  



* login.sh    

  &emsp;&emsp;login.sh 是总控，它会读取 computerInfo.ini，它里面列出了所有需要登录的机器，然后用户选择一台机器，login.sh 就会调用 core.ex 利用 expect 登录选中的机器    

* computerInfo.ini   

  &emsp;&emsp;记录了所有需要登录的机器，其实看到里面记录的ip 也能知道，其实这都是我青牛时期在用的脚本了        

* core.ex   

  &emsp;&emsp;利用 expect 脚本登录可以通过一次跳转登录的机器      

* core_sup_2_user.ex   

  &emsp;&emsp;在 core.ex 上进行了扩展，支持两次跳转登录机器，使用方式如下：   
  ```
  /Users/songbw/auto_login/core_sup_2_user.ex 172.18.254.49 22 18515208389 Sxxxbmwie1201 1 chengguohua lRWjB2YJxeyxO6YD
  ```
  
* core_sup_3_user.ex   

  &emsp;&emsp;在 core_sup_2_user.ex 上进行了扩展，支持三次跳转登录机器   

**展望**  
&emsp;&emsp;目前login.sh 只是用了一次登录的脚本 core.ex，未来有需要也可以去调用 core_sup_2_user.ex 或者 core_sup_3_user.ex  

  

