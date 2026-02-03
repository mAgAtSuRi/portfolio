# portfolio
Personnal project, developping a website to store and manage recipes

venv:
- Create venv in Cookhub/backend: python3 -m venv venv
- Activate venv: source venv/bin/activate
- Install all dependecies inside it: pip install -r requirements.txt

DB:
- Install Postgre: sudo apt install postgresql postgresql-contrib
- Start service: sudo service postgresql start
- connect as super user postgre: sudo -u postgres psql
- reconnect to db psql -h localhost -U tristan -d cookhub

=> inside psql: CREATE DATABASE cookhub;
				CREATE USER cookhub_user WITH PASSWORD 'supersecret';
				GRANT ALL PRIVILEGES ON DATABASE cookhub TO cookhub_user;
- connect to cookhub as user: psql -U user -d cookhub -h localhost


Create .env (backend/.env) file and add the URL_DATABASE= postgresql://cookhub_user:password@localhost:5432/cookhub with Postgre username and password used during creation of the db.


alembic:
	purpose:to allow change to my models like add a column, delete a table etc
	initialise: alembic init alembic
	generate migration file: alembic revision --autogenerate -m "initial schema"
	apply migration to db: alembic upgrade head

FastAPI/Uvicorn: pip install fastapi uvicorn Lancer le serveur: uvicorn app.main:app --reload