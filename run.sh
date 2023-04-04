#!/bin/bash
cwd=$(pwd)
cd /home/ryan/dev/crayon-eater-bot
git pull
source venv/bin/activate
screen -S discordbot -dm python run_bot.py
echo created screen with name discordbot
deactivate
cd $cwd
