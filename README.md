# Find Dining Project Repository

*Project Website (Production)*: https://finddining.ca/ (This is the currently deployed version of the product - Winter 2021 Coop Dev Team)

*Project Website (UAT)*: https://uat.finddining.ca:8444/ (Please include the :8444)

*Project Website (Test)*: https://test.finddining.ca:8443/ (Please include the :8443)

<br/>

### Table of Contents
[Prerequisites](#prerequisite)  
[Development Environment](#run-development-site)  
[Documentation](#documentation)  
[Database](#database)  
[Deployment](#deployment)  
[Permissions and Access](#permissions-and-access)

<br/>

# Project Setup & Overview (Updated Winter 2021)

``` backend ``` contains the Django app project for creating API endpoints that writes/updates/retrieves/remove content from the MongoDB database, and sends data to the Angular frontend.

``` client-server ``` contains the Angular app project for serving static and dynamic content, makes requests to API endpoints defined in Django.

## Prerequisite
- .env file must exist on local computer
    - Must obtain this file from the previous team working on this project
    - Use this to set environment variables for local development
    - Do not commit .env file to repository
- Recommended to work in a linux (or linux-similar) environment (if on windows, consider installing a WSL)
- Install python (3.5, 3.6, 3.7, 3.8, or 3.9)
- Install node.js (10.13.x/12.11.x or later minor version), and npm (6 or higher)

``` 
Angular project was generated with [Angular CLI version 9.1.9]
Django project was generated with [Django version 2.2.20]
```

## Run Development Site
### 1. Run Django Backend
- Install virtualenv somewhere in your Find-Dining-Revamp project local repo and activate it
    - https://sourabhbajaj.com/mac-setup/Python/virtualenv.html (install & activate virtualenv for mac)
    - https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/ (install & activate virtualenv for windows)
- Go to backend folder
- run ``` pip3 install -r requirements.txt ``` (if this is your first time setting up or new packages were added)
- run ``` python manage.py makemigrations ``` and ``` python manage.py migrate ``` (if additions/modifications to the Django models were made; otherwise skip this step)
- run ``` python manage.py runserver ```
- Server should be running at ``` http://localhost:8000 ```

### 2. Run Angular Frontend
- Go to client-server folder
- run ``` npm install ``` (if this is your first time setting up or new packages were added)
- run ``` ng serve ```
- Server should be running at ``` https://localhost:4200 ```

### 3. Visit the Dev Site
- Navigate to ``` https://localhost:4200 ``` to use and test out the running development site

```
Will get 'Your Connection is not Private' warning. Type 'thisisunsafe' on Chrome to bypass this. Press 'Show Details' then 'Visit this website' on Safari to bypass this. Will not occur on test, uat, and production sites due to having verified SSL certificates.
```

## Documentation
### To see the Django documentation:
1. Make sure you've already set up the Django project following the ['Run Django'](#1.-run-django-backend) steps above
2. Once the Django development server is running, navigate to ``` http://localhost:8000/api/swagger/ ``` to view swagger docs or ``` http://localhost:8000/api/redoc/ ``` to view redoc docs

```
Drf-yasg was used to generate Django API documentation
```

### To see the Angular documentation:
1. Make sure you've already set up the Angular project dependencies by running ``` npm install ``` inside of client-server
2. Inside of client-server, run ``` ./node_modules/.bin/compdoc -s ```
3. Once the local server is up, navigate to ``` http://127.0.0.1:8080 ``` to view the Angular docs

```
Compodoc was used to generate Angular documentation
```

## Database
There are four MongoDB databases, each one running in a separate MongoDB container on their respective servers: ``` mongodb-test, mongodb-uat, mongodb-prod ```.

- The .env file will contain the host string, user, and password for the ``` scdining ``` database
- Install MongoDB -v 4.4.x (https://docs.mongodb.com/manual/installation/)
    - Install MongoDB Compass (optional but recommended if you prefer a non-terminal interface)
- Connect to the dev database using the host string in ``` DB_HOST ``` variable from .env
    - mongo "{DB_HOST string}" (if connecting from terminal)
    - Paste DB_HOST string in MongoDB Compass new connection input (if connecting from compass)

## Deployment
Github Actions will run the deployment pipeline upon push to one of the three environment branches ``` test, uat, prod ```. The respective workflow file: ``` deploy.yml ``` is located inside of ``` .github/workflows ``` folder on each environment branch.
  
### Files required for deploying
- Django
  - _settings.py_ in backend/server
  - _wsgi.py_ in backend/server
- Angular
  - _environment.\<environment>.ts_ in client-server/src/environments
    - ``` <environment> can be 'test', 'uat', or 'prod' ```
  - _nginx.conf_ in client-server/nginx
  - _server.crt_ in client-server/ssl
  - _server.key_ in client-server/ssl
    - The .crt and .key files are empty but are required to be present for the Github Actions workflow to execute properly
- Docker
  - _Dockerfile_ in server
  - _Dockerfile_ in client-server
  - _docker-compose.yml_ in CSC-C01-Find-Dining

## Permissions and Access
### Should be able to SSH into (requires UofT general VPN):
- \<utorid>@finddining-uat.utsc.utoronto.ca (server for test & uat environment)
- \<utorid>@finddining.utsc.utoronto.ca (server for prod environment)

```
You can SSH to the servers to examine running docker containers and do necessary troubleshooting
```

### Should be added to:
- Dockerhub Organization: findiningutsc
  - Repositories
    - _finddiningutsc/test_
    - _finddiningutsc/uat_
    - _finddiningutsc/prod_

```
You can view latest image tags of docker images that were built and pushed by either the Github workflow or yourself
```