#!/usr/bin/expect -f

set timeout 60

# ===== 参数解析 =====
# 用法：
# expect jump.exp jump_user jump_host jump_port jump_pass target_host target_user target_pass

if {[llength $argv] != 7} {
    send_user "用法: expect jump.exp jump_user jump_host jump_port jump_pass target_host target_user target_pass\n"
    exit 1
}

set jump_user   [lindex $argv 0]
set jump_host   [lindex $argv 1]
set jump_port   [lindex $argv 2]
set jump_pass   [lindex $argv 3]

set target_host [lindex $argv 4]
set target_user [lindex $argv 5]
set target_pass [lindex $argv 6]

# ===== 启动 SSH =====
send_user "\nINFO Connecting JumpServer...\n"
spawn ssh -p $jump_port $jump_user@$jump_host

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

# ===== MFA 处理（支持多次）=====
proc handle_mfa {} {
    send_user "\nINFO 请输入 MFA 验证码：\n"

    interact {
        \r {
            send "\r"
            return
        }
    }
}

expect {
    "*OTP Code*" {
        handle_mfa
        exp_continue
    }
    "Opt>" {}
    timeout {
        send_user "\nERROR 未进入 JumpServer 菜单\n"
        exit 1
    }
}

# ===== 选择目标机器 =====
send_user "\nINFO 进入目标机器: $target_host\n"
send "$target_host\r"

# ===== 目标机用户名 =====
expect {
    "username:" {
        send "$target_user\r"
    }
    timeout {
        send_user "\nERROR 未出现 username 提示\n"
        exit 1
    }
}

# ===== 目标机密码 =====
expect {
    "*password:" {
        send "$target_pass\r"
    }
    timeout {
        send_user "\nERROR 未出现 password 提示\n"
        exit 1
    }
}

# ===== 成功进入 =====
send_user "\nINFO 登录成功，进入交互模式\n"

interact
