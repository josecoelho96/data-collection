#!/bin/bash

apt update
apt upgrade
apt install postgresql postgresql-contrib

# Install dependencies
sudo pip3 install -r requirements.pip

# Get databse info
echo "Enter database information:"
read -p "Host: " db_host
read -p "Port: " db_port
read -p "Name: " db_name
read -p "User: " db_user
read -s -p "Password: " db_password
echo # New line

# Save info to file
echo "DB = {" > env.py
echo -e "\t'host': '"$db_host"'," >> env.py
echo -e "\t'name': '"$db_name"'," >> env.py
echo -e "\t'user': '"$db_user"'," >> env.py
echo -e "\t'password': '"$db_password"'," >> env.py
echo -e "\t'port': '"$db_port"'," >> env.py
echo "}" >> env.py
echo "TABLE_NAME = 'measurements'" >> env.py

chmod +x deploy.py
python3 deploy.py
echo "Database table created."

# Add collect.py to crontab
chmod +x collect.py
cp collect.py /usr/local/bin
cp env.py /usr/local/bin
cmd="* * * * * /usr/bin/env python3 /usr/local/bin/collect.py"
( crontab -u root -l; echo "$cmd" ) | crontab -u root -
echo "Script added to cron."

echo "All done. Happy data collection :)"