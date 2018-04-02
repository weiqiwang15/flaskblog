#!/usr/bin/env bash

# clone 代码到 /var/www/flaskblog

# ${source_root} 是代码所在目录
source_root="/var/www/flaskblog"

# 换成中科大的源
sudo ln -f -s ${source_root}/sources.list /etc/apt/sources.list
sudo mkdir -p /root/.pip
sudo ln -f -s ${source_root}/pip.conf /root/.pip/pip.conf

# 装依赖
sudo apt-get update
sudo apt-get install -y git python3 python3-pip
sudo apt-get install -y nginx mongodb supervisor redis-server apache2-utils

sudo pip3 install -U pip
sudo pip3 install -r ${source_root}/requirements.txt
sudo pip3 install gunicorn pymysql gevent

# 删掉 nginx default 设置
sudo rm -f /etc/nginx/sites-enabled/*
sudo rm -f /etc/nginx/sites-available/*
# 不要再 sites-available 里面放任何东西
sudo ln -s -f ${source_root}/flaskblog.nginx /etc/nginx/sites-enabled/flaskblog

# 建立一个软连接
sudo ln -s -f ${source_root}/flaskblog.conf /etc/supervisor/conf.d/flaskblog.conf

# 设置文件夹权限给 nginx 用
sudo chmod o+xr /var/www/
sudo chmod -R o+xr ${source_root}

#

# python3 ${source_root}/manage.py create_db
# python3 ${source_root}/manage.py db init
# python3 ${source_root}/manage.py db migrate
# python3 ${source_root}/manage.py db upgrade
# python3 ${source_root}/manage.py create_admin

sudo service supervisor restart
sudo service nginx restart

echo 'succsss'
echo 'ip'
hostname -I
