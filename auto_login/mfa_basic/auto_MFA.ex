#!/usr/bin/expect -f 
set timeout 60

set jump_user "18515208389"
set jump_host "172.18.254.73"
set jump_port "2222"
set jump_pass "Songbowei0801"

# 👉 这里填你的 MFA secret（Base32）
set mfa_secret "OWYQW3ATK7T5HPDW"

set target_host [lindex $argv 0]
set target_user [lindex $argv 1]
set target_pass [lindex $argv 2]
set has_next 0

if {[llength $argv] >= 6} {
    set next_host [lindex $argv 3]
    set next_user [lindex $argv 4]
    set next_pass [lindex $argv 5]
    set has_next 1
}

#set next_host [lindex $argv 3]
#set next_user [lindex $argv 4]
#set next_pass [lindex $argv 5]
#set has_next 1

#exp_internal 1
# ===== 启动 SSH =====
send_user "\nINFO Connecting JumpServer...\n"
#send_user "\ntarget_host:$target_host\ntarget_user:$target_user\ntarget_pass:$target_pass\n next_host:$next_host\nnext_user:$next_user\nnext_pass:$next_pass\n"
spawn ssh -tt -p $jump_port $jump_user@$jump_host
#sleep 1

# ===== JumpServer 密码 =====
expect {
     "*password:" {
        send "$jump_pass\r"
    }
    timeout {
        send_user "\nERROR 未出现 JumpServer 密码提示\n"
        exit 1
    }
}

#spawn ssh -p $jump_port $jump_user@$jump_host
#
#
#expect "*password:"
#send "$jump_pass\r"

#expect "*OTP Code*"

#send_user "\n请现在手动输入手机上的 MFA 验证码：\n"
#
#interact {
#    \r {
#        send "\r"
#        return
#    }
#}
# ===== MFA 阶段 =====
expect {
    "*OTP Code*" {

        # 👉 调用 oathtool 生成验证码
        set otp [exec oathtool --totp -b $mfa_secret]
        after 1000

        send_user "\n自动生成OTP: $otp\n"
        send "$otp\r"

       #exp_continue
    }
}

expect "Opt>"
send "$target_host\r"

expect "username:"
send "$target_user\r"

expect "*password:"
send "$target_pass\r"

# ===== 登录 target_host 后 =====
send_user "\nINFO 已进入第一台机器\n"

# ===== 如果有第二跳 =====
if {$has_next == 1} {

    send_user "\nINFO 准备跳转第二台机器: $next_host\n"
   expect "login"
    # 发起 ssh
    send "ssh $next_user@$next_host\r"

    expect {

        # 第一次连接确认
        "yes/no" {
            send "yes\r"
            exp_continue
        }

        # 密码
        "*password:" {
            send "$next_pass\r"
        }

            -re {.*@.*[$#] $} {
        send_user "\nINFO 第二跳登录成功, no pass 🚀\n"
    }

        timeout {
            send_user "\nERROR 第二跳连接失败（未出现 password）\n"
            exit 1
        }
    }

    send_user "\nINFO 第二跳登录成功 🚀\n"
}


interact
