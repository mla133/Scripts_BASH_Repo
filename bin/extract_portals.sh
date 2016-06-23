#!/bin/bash
# Extracts portal list into two fields (Name|Address) from comm raw input
if [ -z "$1" ]; then
	echo usage: $0 INPUT_FILE 
	exit
fi
SRCF=$1
grep -v ":" $SRCF | sed -e '/Jul */d' | sed -e '/linked/d' | sed -e 's/captured /captured|/g' | sed -e 's/Resonator on /Resonator on|/g' | sed -e 's/ (/|/g' | sed -e 's/)/|/g' | sed -e 's/@/|/g' | sed -e '/is under attack/d' | sed -e '/neutralized by/d' | sed -e '/destroyed by/d' | sed -e 's/the Link /the Link|/g' | cut -d '|' -f 2,3 | sort | uniq
