#!/bin/bash

# Instalar Dependencias

echo -e "\e[36mInstalando dependencias\e[0m"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

apt update

echo -e "\e[36mIntalando transport-http\e[0m"
sudo apt-get install apt-transport-https -y

echo -e "\e[36mInstalando ElasticSearch\e[0m"
sudo apt install elasticsearch -y

echo -e "\e[36mInstalando Kibana\e[0m"
sudo apt install kibana -y

echo -e "\e[36mInstalando logstash\e[0m"
sudo apt install logstash -y

echo -e "\e[36mInstalando Openjdk-11-jre\e[0m"
sudo apt install openjdk-11-jre-headless -y

apt update && apt upgrade 

echo -e "\e[36mInstalando python3\e[0m"
sudo apt install python3-pip -y

echo -e "\e[36mInstalando libreria python river\e[0m"
pip3 install river 

echo -e "\e[36mInstalando libreria python pandas\e[0m"
pip3 install pandas 

echo -e "\e[36mInstalando libreria python elasticsearch\e[0m"
pip3 install elasticsearch 

echo -e "\e[36mInstalando libreria python numpy\e[0m"
pip3 install numpy 
