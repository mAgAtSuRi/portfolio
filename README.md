# portfolio
Personnal project, developping a website to store and manage recipes

DB:
- Install Postgre: sudo apt install postgresql postgresql-contrib
- Start service: sudo service postgresql start
- connect as super user postgre: sudo -u postgres psql
=> inside psql: CREATE DATABASE cookhub;
				CREATE USER cookhub_user WITH PASSWORD 'supersecret';
				GRANT ALL PRIVILEGES ON DATABASE cookhub TO cookhub_user;

Create .env file and add the URL_DATABASE with Postgre username and password