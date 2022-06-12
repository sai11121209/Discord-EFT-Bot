#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl restart discord-bot-eft.service
sudo systemctl status discord-bot-eft.service