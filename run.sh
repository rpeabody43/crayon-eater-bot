#!/bin/bash
cwd=$(pwd)
cd /home/ryan/crayon-eater-bot
git pull
source env/bin/activate
screen -S discordbot -dm python run_bot.py
deactivate
cd $cwd
