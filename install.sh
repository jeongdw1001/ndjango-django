#!/bin/bash

password=
echo -n "MySQL root 계정의 비밀번호:"
stty -echo
read password
echo ""
stty echo
#echo "password=${password}"
echo "***************************************************************"
echo "* Dependencies will be installed shortly *"
echo "***************************************************************"

# Create and activate Python virtual environment for django
py -3.10 -m venv main
source main/Scripts/activate

# Install django main app dependencies using pip
python -m pip install --upgrade pip
pip install -r ./ndjango-django/ndjango/requirements.txt

echo "***************************************************************"
echo "* Created venv: main for Django: main app"
echo "***************************************************************"

# Create MySQL root user 'ndjangoadmin' with password '1234'
mysql -u root -p$password -e "CREATE USER 'ndjangoadmin'@'localhost' IDENTIFIED BY '1234';"
mysql -u root -p$password -e "GRANT ALL PRIVILEGES ON *.* TO 'ndjangoadmin'@'localhost' WITH GRANT OPTION;"
mysql -u root -p$password -e "FLUSH PRIVILEGES;"

# Create MySQL schema 'contents01' using 'ndjangoadmin' user
mysql -u ndjangoadmin -p1234 -e "CREATE SCHEMA contents01 CHARACTER SET utf8 COLLATE utf8_general_ci;"

echo "***************************************************************"
echo "* Created mysql user: ndjangoadmin with password: 1234"
echo "* Created mysql schema: contents01 for Django"
echo "***************************************************************"

# Run Django's makemigrations and migrate commands
cd ndjango-django/ndjango
python manage.py makemigrations
python manage.py migrate

# Run the Python Script to insert icon and korean recipe data
cd ../data/db_initializer
python icon.py
python kor_recipe.py

echo "* Initialized Django app"

# Deactivate the virtual environment
deactivate

# Create and activate Python virtual environment for fastapi
cd ../../../
py -3.10 -m venv kor-recipe
source kor-recipe/Scripts/activate

# Install Fastapi dependencies using pip
python -m pip install --upgrade pip
pip install -r ./ndjango-django/recipe-recommender2/requirements.txt

# Deactivate the virtual environment
deactivate

echo "***************************************************************"
echo "* Created venv: kor-recipe for Fastapi: kor recipe-recommender"
echo "***************************************************************"

# Create and activate Python virtual environment for flask
py -3.10 -m venv photo-predict
source photo-predict/Scripts/activate

# Install Flask dependencies using pip
python -m pip install --upgrade pip
pip install -r ./ndjango-django/photo_predict/requirements.txt

# Deactivate the virtual environment
deactivate

echo "***************************************************************"
echo "* Created venv: photo-predict for Fastapi: photo predict"
echo "***************************************************************"

echo "설치가 완료되었습니다."
echo "django, fastapi, flask 쉘스크립트를 실행해주세요"

