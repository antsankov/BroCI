#!/bin/bash

sudo apt-get update
sudo apt-get install htop slurm cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev
cd bro-2.3
sudo ./configure 
sudo make
sudo make install
pwd
export PATH=/usr/local/bro/bin:$PATH
cd .. 
#copy my experiment scripts in 
sudo rm /usr/local/bro/share/bro/policy/misc/capture-loss.bro
sudo cp bro_experiments/*.bro /usr/local/bro/share/bro/policy/misc

#remove the current local.bro loader
sudo rm /usr/local/bro/share/bro/site/local.bro

#copy the correct version of local.bro to the proper site. 
sudo cp bro_experiments/local.bro  /usr/local/bro/share/bro/site/

#config the right editor
sudo update-alternatives --config editor

#remove 'Defaults       secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"'
sudo visudo
echo 'Bro is good to go!' 