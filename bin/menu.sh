#!/bin/bash
OPTIONS="Batch Live Trans Quit"
select opt in $OPTIONS; do
  if [ "$opt" = "Quit" ]; then
    echo Done
    exit
  elif [ "$opt" = "Batch" ]; then
    $HOME/scripts/rb | grep batch_pulses --color
  elif [ "$opt" = "Live" ]; then
    $HOME/scripts/ltemp
  elif [ "$opt" = "Trans" ]; then
    $HOME/scripts/rd | grep trans_ --color
  else
    clear
    echo Bad Option
  fi
done
