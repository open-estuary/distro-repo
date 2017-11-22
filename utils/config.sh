#!/bin/bash

echo "Begin configure build enviroment."

if [ ! -f ~/.rpmmacros ]; then 

    wget -O ~/ https://github.com/open-estuary/distro-repo/tree/master/utils/config/.rpmmacros
    #sudo cp /home/huangjinhua/.rpmmacros ~/.rpmmacros
fi

if [ ~ -f ~/.gnupg/gpg.conf ]; then
    wget -O ~/.gnupg/ https://github.com/open-estuary/distro-repo/tree/master/utils/config/gpg.conf
    #sudo cp /home/gpg.conf ~/.gnupg/gpg.conf
fi

gpg --import /home/ESTUARY-GPG-SECURE-KEY


