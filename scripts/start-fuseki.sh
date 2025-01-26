#!/bin/bash
#cd ./apache-jena-fuseki-5.2.0
#java -jar fuseki-server.jar #--host=0.0.0.0

#!/bin/bash
# Mise à jour et démarrage de Fuseki
sudo apt update
sudo apt install default-jre -y
cd ./apache-jena-fuseki-5.2.0
#cd /workspaces/Web_Semantics_project/apache-jena-fuseki-5.2.0
java -jar fuseki-server.jar --update --mem /dataset &
