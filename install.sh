#!/bin/bash

basepath=$(dirname $0)

cd ${basepath}

INSTALLATION() {
    echo -e "\e[0;36m"You must be root to installing dependencies, copy files to \'/usr/bin\' directory and \'chomd +x to /usr/bin/bianance_desklets/*\'"\e[0m"
    
    sudo apt install python3 python3-pip libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 -y
    
    if [    "$?" = "0" ];then
        echo -e "\e[0;32m"Dependencies Installation Was Successful."\e[0m"
    else
        echo -e "\e[0;31m"Dependencies Installation Is Failed"\e[0m"
        exit 1
    fi

    echo -e "\e[0;36m"Preparing..."\e[0m"

    sudo mkdir /usr/bin/bianance_desklets

    sudo cp $(pwd)/binance.py $(pwd)/coin.png /usr/bin/bianance_desklets
           
    sudo python3 -m venv /usr/bin/bianance_desklets/venv
       
    pip3 install requests pycairo PyGObject
    
    cp $(pwd)/binance.desktop  $HOME/.config/autostart

    sudo chmod +x /usr/bin/bianance_desklets/*
    
    echo -e "\e[0;36m"Preparing Completed..."\e[0m"
    
    echo -e "\e[0;36m"Starting Desklet..."\e[0m"

    read -p "Application need reboot to run. reboot?(default=No)/y(yes)" REBOOT

    REBOOT=${REBOOT:-no}

    if [    "$REBOOT" = "y" ] || [    "$REBOOT" = "Y" ] || [    "$REBOOT" = "yes" ] || [    "$REBOOT" = "YES" ] || [    "$REBOOT" = "Yes" ];then
        sudo reboot -f
    else
        exit 0
    fi   
}

INSTALLATION
