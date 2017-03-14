#!/bin/bash

# Splash and copyright
echo " "
echo " _____         _           _       _____ __  __  ____  "
echo "|_   _|__  ___| |__  _ __ (_)_ __ |  ___|  \/  |/ ___| "
echo "  | |/ _ \/ __| '_ \| '_ \| | '_ \| |_  | |\/| | |     "
echo "  | |  __/ (__| | | | | | | | |_) |  _| | |  | | |___  "
echo "  |_|\___|\___|_| |_|_| |_|_| .__/|_|   |_|  |_|\____| "
echo "                            |_|                        "
echo
echo "    http://www.technipfmc.com"
echo
echo "All software on this device is one of:"
echo "     - Open source software governed by various open source licenses"
echo "     - Licensed from the copyright holder"
echo "     - Copyright FMC Technologies, 2015"
echo
# info
echo
echo "To set the (permanent) IP address:"
echo "     connmanctl services"
echo "     connmanctl config <service> --ipv4 manual <ip> <subnet> <gateway>"
echo
alias ls='ls --color'
export PATH=$PATH:/home/root/bin
