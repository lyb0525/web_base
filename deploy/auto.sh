#!/usr/bin/env bash


# 安装系统依赖
sudo apt-get install supervisor
sudo apt-get install git python-setuptools libmysqlclient-dev libpython2.7-dev libjpeg8-dev libfreetype6-dev zlib1g-dev nginx
sudo apt-get install mysql-server-5.6 #密码为root
sudo apt-get install language-pack-zh-hant language-pack-zh-hans


# 安装python依赖
sudo apt-get install python-pip # 或者 sudo easy_install pip

sudo pip install virtualenvwrapper
echo "source `which virtualenvwrapper.sh`" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv ss # security-static
workon ss
pip install -r requirements.txt

# 部署nginx配置文件
sudo rm /etc/nginx/sites-enabled/default
sudo cp deploy/nginx.conf /etc/nginx/sites-available/security
sudo ln -sf /etc/nginx/sites-available/security /etc/nginx/sites-enabled/security
sudo nginx -s reload

# 部署mysql配置文件
# sudo cp deploy/mysql.cnf /etc/mysql/conf.d/security.cnf
# sudo service mysql restart

# ok, let's go
sudo supervisorctl reload # 如果失败，尝试重启服务sudo service supervisor restart
