#!/bin/bash
OPTIONS="Hello Quit"
select opt in $OPTIONS; do
  if [ "$opt" = "Quit" ]; then
    echo Done
    exit
  elif [ "$opt" = "Hello" ]; then
    echo Hello World
  else
    clear
    echo Bad Option
  fi
done
