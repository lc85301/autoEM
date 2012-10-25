#!/usr/bin/env bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin 
export PATH

filename="./test.son"
remote_loc="~/autoEM/"
remote_filename="test.son"
server="r101008@140.112.19.172"

#scp	$filename $server:$remote_loc$remote_filename
#ssh -t $server 'screen -dm -S autoEM ~/autoEM/command.sh'
#ssh -t $server '~/autoEM/command.sh'
#ssh $server 'screen -S autoEM -d -m ~/autoEM/command.sh'
#ssh -f $server 'source ~/.bashrc; em ~/autoEM/test.son'
ssh -f $server 'source ~/.bashrc; nohup em ~/autoEM/test.son'
