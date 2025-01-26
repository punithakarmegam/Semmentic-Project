#!/bin/bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install SPARQLWrapper

./scripts/start-fuseki.sh & ./scripts/node_install.sh 
#& ./scripts/start-http-server.sh