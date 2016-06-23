#!/bin/sh

ps -A | grep delivery 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
	pkill delivery
fi

ps -A | grep criticals 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill criticals 
fi

ps -A | grep smithcommd 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill smithcommd
fi

ps -A | grep node 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill node
fi

ps -A | grep json_write 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill json_write
fi

ps -A | grep socat 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill socat
fi

ps -A | grep json_read 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill json_read
fi

ps -A | grep json_hash 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill json_hash
fi

ps -A | grep write_file.sh 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill write_file.sh
fi

ps -A | grep modbusd 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill modbusd
fi

ps -A | grep Promass 2>1 > /dev/null
if [[ $? -eq 0 ]]; then
        pkill Promass
fi
