#!/bin/zsh

dir=`pwd`
while IFS="" read -r p || [ -n "$p" ]
do
  x=${p:0:-4}
  printf '%s%s\n' "$dir/development-docs/$x"
done < list_of_files.txt
