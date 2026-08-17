#!/bin/bash
file="/Users/songbw/auto_login/basic_jump/computerInfo.ini"
#显示机器信息 过滤第一行和空行
awk '{if (NR > 1 && $1 != ""){printf "%-2s %-45s %-15s \n","("NR-1")",$5,$1}}' $file
echo "please choose which machine to login:"
read number
number=$[number+1]
#将信息存入变量
read ip port user password <<< $(echo `awk 'NR=="'$number'"{print $1,$2,$3,$4}' $file`)
echo $password
/Users/songbw/auto_login/core.ex $ip $port $user $password
