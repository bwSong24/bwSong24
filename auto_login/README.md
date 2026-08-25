早期版本1 -- 直接shell    
login.sh     
core.ex   
computerInfo.ini     

直接 .zshrc 中控制 alias aoel='/Users/songbw/auto_login/login.sh'，    
login.sh 一方面调用 core.ex 脚本，一方面读取 computerInfo.ini 中的机器信息，让我选择机器    
这个版本的优势是很突出的，因为是直接在 shell 中执行的，所以很稳定

早期版本2 -- 发现了 item 中的 profile  
core_sup_2_user.ex  
core_sup_3_user.ex   
core.ex   

这3个脚本都有用，分别支持一个用户、两个用户、三个用户  

core_sup_3_user.ex 是用样例

```
/Users/songbw/auto_login/core_sup_3_user.ex 172.18.254.49 22 18515208389 Songbowei0801 1 chengguohua lRWjB2YJxeyxO6YD 10.100.34.41 huangmingming lsui38%UIh3s
```



目前版本  -- MFA(GPT时代了)  
jump.sh，目前支持一跳和两跳     
manue_MFA_inter.ex (这个其实已经很少用了，除非调试的时候，有自动的，谁还用手动的啊)

```
/Users/songbw/auto_login/mfa_basic/manue_MFA_inter.ex 18515208389 172.18.254.73 2222  Songbowei0801 10.100.34.42 huangmingming lsui38%UIh3s
```



manue_MFA.ex  (后来改名为 auto_MFA.ex)

使用方法：
外围调用 jump.sh ，jump.sh里面调用 manue_MFA.ex，登录哪台机器，是通过传递参数实现的    
manue_MFA_inter.ex 是交互版本，需要我手动输入 MFA，其实手动输入 MFA 的版本挺稳的  
auto_MFA.ex 是自动版本，就是MFA 码是通过执行 oathtool 实现的

* 使用样例

```
/bin/bash -lc "~/auto_login/jump.sh 10.189.1.129 bwsong 321songbowei"
/bin/bash -lc "~/auto_login/jump.sh 10.100.34.42 huangmingming lsui38%UIh3s 10.100.34.41 wangtiezheng lsui38%UIh3s"
```



* 注意

因为 jump.sh 的这一版本，密码是写在 jump.sh 里的，所以密码里一旦出现一些特殊字符，有可能就不行，密码需要单独加一个单引号，如下(214机器和34机器都是)，这也是，我后来去做 jump_secure.exp 的原因，就是把密码都移到配置文件中，这样就不会出现这样的问题    

```
/bin/bash -lc "~/auto_login/jump.sh 10.189.1.129 bwsong 321songbowei 10.189.177.214 wangtiezheng 'J7bD5&hL2mQ9wE6'"
/bin/bash -lc "~/auto_login/jump.sh 10.100.34.34 songbowei 'fz4!yO$KmMsn@h62ki*FXYD!UwMNO@Ja'"
```







一些基础知识(expect)：   
expect 的核心规则    

```
一个 expect 块：
👉 匹配到某个分支
👉 执行代码
👉 默认就结束（退出 expect）
```

也就是说 
```
expect {
    A { ... exp_continue }
    B { ... exp_continue }
    C { ... }   ← 没有 exp_continue
}
```

执行流程：  
```
匹配 A → 继续等
匹配 B → 继续等
匹配 C → expect 结束 ✅
```
exp_continue 的含义是 "继续等"，但前提是得匹配上规则   

因为我的 expec 中有   
```
-re "yes/no" {
    send "yes\r"
    exp_continue
}
```


那么，我现在基本没有 yes/no，这会不会卡住？
答案是不会  

这个分支只有在：   

真的出现 yes/no  
才会触发    


四、你可以把 expect 想成“状态机”

你现在这段代码，本质是：

```
209     expect {
210
211         # 第一次连接确认
212         "yes/no" {
213             send "yes\r"
214             exp_continue
215         }
216
217         # 密码
218         "*password:" {
219             send "$next_pass\r"
220         }
221
222             -re {.*@.*[$#] $} {
223         send_user "\nINFO 第二跳登录成功, no pass 🚀\n"
224     }
```

进入 SSH 后：
```
状态1：yes/no → 处理
状态2：password → 输入
状态3：shell → 成功结束
```




