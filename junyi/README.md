# junyi

Python 3.5.2
Django 1.10.2

## Setup

### Create virtualenv

macOS

    pyvenv venv

### Change virtualenv

	source venv/bin/activate

### Install packages

	cd ~/junyi-webserver
	pip install -r reuqirements.txt

### Postgresql

Install Postgresql

	brew install postgresql

Create user

	createuser -P -e junyi_user
	Enter password for new role: junyi
	Enter it again: junyi
	CREATE ROLE junyi_user PASSWORD ...

Create database

	createdb junyi_db

Grant

	$: psql
	postgres=# GRANT ALL PRIVILEGES ON DATABASE junyi_db TO junyi_user;

Initial Database

	python manage.py migrate --setting=junyi.settings.local

### Redis

Install Redis

	brew install redis

## Start Server

### Redis Server

    redis-server /usr/local/etc/redis.conf

### Local Server

	python manage.py runserver --setting=junyi.settings.local
