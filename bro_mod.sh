#!/bin/bash

#This is used when we made some changes to experiments nad we don't want to reinstall everything
echo 'Starting bro_mod'
#update all of the experiments in the git repo 
#git pull

#remove the default caputre-loss.bro script
sudo rm /usr/local/bro/share/bro/policy/misc/capture-loss.bro
#copy the bro scripts in the experiments directory to the misc folder for them to be tested 
sudo cp *.bro /usr/local/bro/share/bro/policy/misc

#remove the current local.bro loader
sudo rm /usr/local/bro/share/bro/site/local.bro

#copy the correct version of local.bro to the proper site. 
sudo cp local.bro  /usr/local/bro/share/bro/site/
echo 'Ending bro_mod'
