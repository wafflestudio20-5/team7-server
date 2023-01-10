#!/bin/sh     
# sudo git pull origin master
# sudo pip3 install -r requirements.txt

echo "hello!"

cd $(dirname "$0")
echo "현재경로"
pwd //현재경로

echo "chmod deploy.sh"
chmod +x ./deploy.sh

echo "installing python..."
sudo apt update
sudo apt python3.8

echo "installing pip..."
sudo apt-get -y install python3-pip

echo "installing virtualenv"
sudo pip3 install virtualenv 

echo "installing gunicorn"
sudo python3 -m pip install gunicorn

# echo "activate venv..."
# source team7elog/bin/activate

echo "install package..."
cd velog
sudo python3 -m pip -y install -r "requirements.txt"

# echo "install django..."
# python3 -m pip install django==4.1

#echo "install pymysql..."
#python3 -m pip install pymysql

echo "installing drf_yasg..."
sudo python3 -m pip install drf_yasg

echo "collect static..."
python3 manage.py collectstatic

echo "make migrations..."
python3 manage.py makemigrations

echo "apply migration..."
python3 manage.py migrate

#echo "move location to project..."
#cd velog

echo "gunicorn..."
nohup gunicorn --bind 0.0.0.0:8000 velog.wsgi:application 

# sudo systemctl restart nginx
# sudo systemctl restart gunicorn

