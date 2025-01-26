#!/bin/bash
cd ./app_node
sudo apt update
sudo apt install -y nodejs npm
sudo npm install express body-parser axios
nodejs server.js
