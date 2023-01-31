#!/bin/sh     
# sudo git pull origin master
# sudo pip3 install -r requirements.txt

echo "hello!"

cd $(dirname "$0")
echo "현재경로"
pwd //현재경로

echo "change user to root"
sudo su

echo "chmod velogapp"
chmod +x ./velog/velogapp

echo "chmod authentication"
chmod +x ./velog/authentication

echo "chmod deploy.sh"
chmod +x ./deploy.sh

echo "chmod templates"
chmod +x ./velog/templates/
chmod +x ./velog/templates/account/
chmod +x ./velog/templates/account
chmod +x ./velog/templates/socialaccount/
chmod +x ./velog/templates/socialaccount
chmod +x ./velog/templates/loaders/
chmod +x ./velog/templates/loaders
chmod +x ./velog/templates/account/messages/
chmod +x ./velog/templates/account/messages/logged_in.txt

chmod 777 ./velog/templates/
chmod 777 ./velog/templates/account/
chmod 777 ./velog/templates/account
chmod 777 ./velog/templates/socialaccount/
chmod 777 ./velog/templates/socialaccount
chmod 777 ./velog/templates/loaders/
chmod 777 ./velog/templates/loaders
chmod 777 ./velog/templates/account/messages/
chmod 777 ./velog/templates/account/messages/logged_in.txt

echo "installing python..."
sudo apt update
sudo apt-get install python3.8

echo "installing pip..."
sudo apt-get install python3-pip

echo "installing virtualenv"
sudo pip3 install virtualenv 

echo "installing gunicorn"
sudo python3 -m pip install gunicorn

echo "installing environ"
sudo python3 -m pip install django-environ

echo "activate venv..."
. /home/ubuntu/team7elog/bin/activate

echo "install package..."
cd velog
sudo python3 -m pip install -r "requirements.txt"

echo "install django..."
python3 -m pip install django==4.1

echo "install pymysql..."
python3 -m pip install pymysql

echo "installing drf_yasg..."
sudo python3 -m pip install drf_yasg

echo "installing coresheaders..."
sudo python3 -m pip install django-cors-headers

echo "collect static..."
yes | python3 manage.py collectstatic

echo "make migrations..."
yes | python3 manage.py makemigrations

echo "apply migration..."
python3 manage.py migrate

#echo "move location to project..."
#cd velog

echo "gunicorn..."
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

echo "nginx..."
sudo systemctl restart nginx
sudo systemctl status nginx
# sudo systemctl restart gunicorn

