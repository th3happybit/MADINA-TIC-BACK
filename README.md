# Madina-Tic-backend
a django based backend for madina-tic project

## Deployment:

### Manual deployment
	- requirements:
		1. python 3.8 and pip
	- setup the backend:
		- install django and other requirements:
			- `sudo pip install -r requirements.txt`
		- run server:
			- `./manage.py runserver`

### Docker deployment:
	- requirements:
		1. install docker deamon [docs](https://docs.docker.com/install/).
		2. install docker-compose tool [docs](https://docs.docker.com/compose/install/).
	1. build the backend image:
		- `sudo docker build -t madina-tic/backend:0.1 .`
		or :
		- `sudo docker build -f Dockerfile -t madina-tic/backend:0.1 /full/path/to/`
	2. change the settings of the database engine to sqlite.
	3. run the container:
		- `sudo docker run -d -p 8000:8000 madina-tic/backend:0.1`

## Docs

1. First login as an admin:

	`http://0.0.0.0/api/admin/`
	
		- creds:
			username: admin
			password: blackholE

2.	docs route:
	`http://0.0.0.0/api/swagger/`
