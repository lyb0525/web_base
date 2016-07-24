#!/usr/bin/env bash
# 安装系统依赖
# sudo apt-get install supervisor
# sudo apt-get install git python-setuptools libmysqlclient-dev libpython2.7-dev libjpeg8-dev libfreetype6-dev zlib1g-dev nginx
# sudo apt-get install mysql-server-5.6 #密码为root
# sudo apt-get install language-pack-zh-hant language-pack-zh-hans
#
#
# # 安装python依赖
# sudo apt-get install python-pip # 或者 sudo easy_install pip
#
# sudo pip install virtualenvwrapper
# echo "source `which virtualenvwrapper.sh`" >> ~/.bashrc
# mkvirtualenv ss
# workon ss
# pip install -r requirements.txt
#
SYSTEM=`uname -s`    #获取操作系统类型，我本地是linux
NIGNX_PATH=
if [ $SYSTEM = "Linux" ] ; then     #如果是linux的话打印linux字符串
    NIGNX_PATH="/etc/nginx/"
    echo "Linux"
elif [ $SYSTEM = "FreeBSD" ] ; then
    echo "FreeBSD"
elif [ $SYSTEM = "Solaris" ] ; then
    echo "Solaris"
elif [ $SYSTEM = "Darwin" ] ; then
    NIGNX_PATH="/usr/local/etc/nginx/"
    echo "Darwin"
else
    echo "What?"
fi     #ifend
# 部署nginx配置文件
if [ ${NIGNX_PATH} ]; then
    if [ -f  ${NIGNX_PATH}"sites-enabled/default" ]; then
        sudo rm ${NIGNX_PATH}"sites-enabled/default"
    fi
    sudo cp deploy/nginx.conf ${NIGNX_PATH}"sites-available/plat_nginx.conf"
    sudo ln -sf ${NIGNX_PATH}"sites-available/plat_nginx.conf" ${NIGNX_PATH}"sites-enabled/plat_nginx.conf"
    sudo nginx -s reload
else
    echo "pass"
fi
