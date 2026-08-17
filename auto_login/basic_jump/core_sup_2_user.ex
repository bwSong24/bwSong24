#!/usr/bin/expect
set ip [lindex $argv 0]
set port [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set seq [lindex $argv 4]
set username1 [lindex $argv 5]
set password1 [lindex $argv 6]
set timeout -1
#puts $username1
#puts $password1
spawn ssh -p $port $username@$ip
expect {
    "yes/no" {send "yes\r";exp_continue}
    "*assword" {send "$password\r";}
}
expect "Select server"
send "$seq\r"
expect "Input account"
send "$username1\r"
expect "*assword"
send "$password1\r"
#expect {
#    "Select server" {send "$seq\r";exp_continue}
#    "*account" {send "$username1\r";exp_continue}
#    "*assword" {send "$password1\r";exp_continue}
#}
interact
