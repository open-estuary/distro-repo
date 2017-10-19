#!/bin/bash

echo "Begin configure build enviroment."

if [ ! -f ~/.rpmmacros ]; then 
    sudo cp /home/huangjinhua/.rpmmacros ~/.rpmmacros
fi

sudo cp /home/gpg.conf ~/.gnupg/gpg.conf
gpg --import /home/ESTUARY-GPG-SECURE-KEY


