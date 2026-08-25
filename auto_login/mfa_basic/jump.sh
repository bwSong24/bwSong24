#!/bin/bash

echo $#
#参数要大于2个 否则退出，这个用于参数判断
if [ $# -gt 3 ];then
	echo  "two jump"
    /Users/songbw/auto_login/mfa_basic/auto_MFA.ex \
$1 $2 $3 \
$4 $5 $6
else
    /Users/songbw/auto_login/mfa_basic/auto_MFA.ex $1 $2 $3
fi

