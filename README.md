# Find Dining Project Repository

*Project Website (Production)*: https://finddining.ca/ (This is the currently deployed version of the product - Winter 2021 Coop Dev Team)

*Project Website (UAT)*: https://uat.finddining.ca:8444/ (Please include the :8444)

*Project Website (Test)*: https://test.finddining.ca:8443/ (Please include the :8443)

### Table of Contents
[Prerequisites](#prerequisite)  
[Development Environment](#setup-development-environment)  
  - [Setup](#setup-development-environment)
  - [Authentication](#authentication-overview)  
  - [Backend Overview](#backend-overview)  
  - [Frontend Overview](#frontend-overview)  
  - [Unit Tests](#running-Django-unit-tests)

[Documentation](#documentation)  
[Database](#database)  
[Permissions and Access](#permissions-and-access)  
[AODA](#aoda)  
[Deploying Changes](#deployment)  

### Contact Info
minqi.zhang@mail.utoronto.ca - Min Qi Zhang (frontend)
 - majority of frontend pages, components, services, and constants
 - frontend form validation, mobile-friendly css
 - AODA compliance specialist
  
isaac.mou@mail.utoronto.ca - Isaac Mou (backend)
- frontend httpinterceptor, frontend auth services, frontend guards
- backend authentication (login, signup, jwt tokens)
- backend for news articles, sduser, login_audit

jayden.tse@mail.utoronto.ca - Jayden Tse (backend/deployment)
- admin restaurant graphs, github actions, docker containers
- backend for subscriber_profile
- backend settings.py for each environment

zi.yu@mail.utoronto.ca - Jenny Yu (backend/frontend)
- backend for restaurant, restaurant_owner, newsletter
- frontend news articles, frontend subscriber_profile, assist with mobile-friendly css and frontend components typescript
- swagger documentation, compodoc documentation

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
- Install python (v3.5, v3.6, v3.7, v3.8, or v3.9)
- Install node.js (v10.13.x/12.11.x or later minor version), and npm (v6 or higher)
- Install mongodb (v4.4.x) https://docs.mongodb.com/manual/installation/

``` 
Angular project was generated with [Angular CLI version 9.1.9]
Django project was generated with [Django version 2.2.20]
```

<br/>

## Setup Development Environment
### 1. Run Django Backend
Install virtualenv somewhere in your Find-Dining-Revamp project local repo and activate it
  - https://sourabhbajaj.com/mac-setup/Python/virtualenv.html (install & activate virtualenv for mac)
  - https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/ (install & activate virtualenv for windows)

Activate the virtualenv for this project.

Set environment variables from .env file.

Install project dependencies (if first-time setup or new dependencies were added):
```
$ cd backend
$ pip3 install -r requirements.txt
```
Make and apply migrations (if models were modified or new ones were added):
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Start the development server:
```
$ python manage.py runserver
```
Server should be running at ``` http://localhost:8000 ```

Navigate to ``` http://localhost:8000/api/fd-admin ``` to view admin site (get admin credentials from member of previous team)

<br/>

### 2. Run Angular Frontend
Install project dependencies (if first-time setup or new dependencies were added):
```
$ cd client-server
$ npm install
```
Start the development server:
```
$ ng serve
```
Server should be running at ``` https://localhost:4200 ```

Navigate to ``` https://localhost:4200 ``` to use and test out the development site

```
Will get 'Your Connection is not Private' warning.
Type 'thisisunsafe' on Chrome to bypass this.
Press 'Show Details' then 'Visit this website' on Safari to bypass this.
Will not occur on test, uat, and production sites due to having verified
SSL certificates.
```
![website landing page](https://lh3.googleusercontent.com/pw/ACtC-3c0wp_tfbNzwTKhBP1D9rbh8fK1PkMP2-66hgP6-BjGgiTPFJtyLR6BSOmK9vXa7V7QAYXohmr5RB7r-AmChhxtjYAzIoYxr7jBA63LJe-BqtVXm6Xup5Uq9CBB-dNhcp5tgdik1tgQgZimZlQr_yAB=w1370-h873-no?authuser=0)

### Authentication overview

### Backend overview
Backend settings.
```
- server/ (set project settings from environment variables)
```
Django apps for API CRUD operations.
```
- article/ (news articles get, create)
- newsletter/ (newsletter signup)
- restaurant/ (restaurants, food, posts, and favourites operations)
- restaurant_owner/ (restaurant owner profile get, create, modify)
- sduser/ (login, signup, token refresh, etc)
- subscriber_profile/ (subscriber profile get, create, modify)
```
Utility function folders.
```
- google/ (google analytics, google sheets for mass mailing)
- index/ (send mail for verification)
- oauth2/ (3rd party login and signup)
- utils/ (many helper functions: validators, exception handler, etc)
```
Admin site specific folders.
```
- admin_honeypot/ (for guarding admin login portal)
- image/ (for admin site image handling)
```
Django served pages folders.
```
- static/ (admin and django served pages static files)
- templates/ (admin and django served pages HTML files)
```

<br/>

### Frontend overview
User displayed pages (what you'd see when visiting the website).
```
- src/app/pages/ (displaying pages based on data from backend)
  - about-us/
  ...
  - thankyou-page/
```
Child components used on displayed pages.
```
- src/app/components/ (ie. restaurant cards on all-listings page)
  - article-common-card/
  ...
  - virtual-scrolling/
```
Services for making http requests to backend.
```
- src/app/_services/ (makes requests to backend server)
  - article.service.ts
  ...
  - user.service.ts
```
Auth guards for page protection and http interceptor.
```
- src/app/_helpers/
  - auth.guard.ts (guards against non logged-in users)
  - auth.interceptor.ts (sends access token in http requests and refreshes token if
    expired)
  - ro.guard.ts (guards against non-RO users)
  - secure.guard.ts
```
Form validators.
```
- src/app/_validation/ (for validating form input)
  - dishValidator.ts
  ...
  - userValidator.ts
```
Angular frontend deployment.
```
- src/environments/ (environment.ts files)
- nginx/ (nginx.conf file)
- ssl/ (server.crt and server.key files *LEAVE EMPTY AND DO NOT DELETE)
```

<br/>

### Running Django unit tests
Activate your virtualenv, then run the following commands to run a single test case.
```
$ cd backend
$ pytest {{ app }}/{{ tests.py }}::{{ test_class }}::{{ test_case_function }}
```
To run all tests for all apps.
```
$ cd backend
$ pytest
```
Example usage.
```
$ cd backend
$ pytest restaurant/tests.py::DraftRestaurantTestCases::test_insert_restaurant_draft_valid
```

<br/>

## Documentation
### To see the Django documentation:
Make sure you've already set up the Django project following the ['Run Django Backend'](#setup-development-environment) steps above

Activate your virtualenv.

Set environment variables from .env file.

Run Django development server.
```
$ cd backend
$ python manage.py runserver
```
View documentation.
- ``` http://localhost:8000/api/swagger/ ``` to view swagger docs or
- ``` http://localhost:8000/api/redoc/ ``` to view redoc docs
![swagger documentation](https://lh3.googleusercontent.com/pw/ACtC-3cMxyA5vjJLqF9oeAyopG6VpMze2kj-37Rv2Z7H29PjX-NaQ3Nju-wcHy4Rj4pJZ_fwwZpFdyg_w_kMTtO33Fg9GdffZhp9U-uVZp4ThITHjmkKZBsx0wIYk24eKrCHSpWXe97CJem1sWCrtxiiFDpW=w1370-h873-no?authuser=0)
![redoc documentation](https://lh3.googleusercontent.com/pw/ACtC-3e1mes_LlbBhpgtHODdvl3Ys0nM6rS5wagdoYPU7k30z5K6bNkGdUZkVGvfdC1RLdrt1VAHISVjhEe9F8rCID4MxQb91HoV5korsLcrfprNsDhUMMFZnb_XV7fMwrGz1rkyx4OEkhtjMR2IXlqa4OVI=w1370-h873-no?authuser=0)

Drf-yasg was used to generate Django API documentation

<br/>

### To see the Angular documentation:
Make sure you've already set up the Angular project dependencies.
```
$ cd client-server
$ npm install
```
Generate the compodoc documentation.
```
$ run npm compdoc
```
Start the development server for compodoc documentation.
```
$ cd client-server
$ ./node_modules/.bin/compdoc -s
```
View documentation.
- ``` http://127.0.0.1:8080 ``` to view Angular compodocs
![compdoc documentation](https://lh3.googleusercontent.com/pw/ACtC-3cSU7rh0Eitipurpet7v0VNRag4gDagt7X7FBRDQ1mD2GkrFS04ekxmkPFjRc9VN78z5iMuhsxAQv4rFr-QevCgdw_YYQouZ8Uewr6LRy-eH1MvjIh4UvA7KwS2-QW0ShNRKTtKPnlYJgSBb3iT_215=w1370-h873-no?authuser=0)

Compodoc was used to generate Angular documentation

<br/>

## Database
There are four MongoDB databases, each one running in a separate MongoDB container on their respective servers.
```
mongodb-test (test.finddining.ca:8443)
mongodb-uat (uat.finddining.ca:8444)
mongodb-prod (finddining.ca)
```

The .env file will contain the host string, user, and password for the ``` scdining ``` dev database

### MongoDB Installation
Install MongoDB v4.4.x
- https://docs.mongodb.com/manual/installation/

Install MongoDB Compass *optional but recommended if you prefer a more graphical interface
- https://www.mongodb.com/products/compass

<br/>

### MongoDB Connection
Connect to the dev database using the host string in ``` DB_HOST ``` variable from .env

If connecting from a terminal.
```
$ mongo "{{ DB_HOST }}"
$ use scdining
```
If connecting from MongoDB Compass
```
Paste DB_HOST string in MongoDB Compass new connection input
```
![mongodb compass new connection](https://lh3.googleusercontent.com/pw/ACtC-3dDeBrbiMLiF36REo9DJZe5zpkK4-OcEFlHe_0xaRA0HFNf7BArelVs47_O9G3dDNL79D2eHrFss12CRgIX9Ud_bm2-NwjM9xRsCr5k_5KJSb4ROgHVT183J1eh7-IpwLXspjq3i4fboZOyRx3Irm8r=w1370-h873-no?authuser=0)

## Permissions and Access
### Should be able to SSH into (requires UofT general VPN):
- \<utorid>@finddining-uat.utsc.utoronto.ca (test & uat server)
- \<utorid>@finddining.utsc.utoronto.ca (prod server)

```
You can SSH to the servers to examine running docker containers and do necessary troubleshooting
```

### Should be added to:
Google Cloud Console (project name: scdining-winter2021)
```
Please ask a member of the Find Dining team (that can login with info@finddining.ca)
to add you as an owner of the project
```
- https://console.cloud.google.com/
- GCP services being used:
    - Google Cloud Storage (for storing images and videos)
    - Geocoding (for getting latitude, longitude coordinates of a location)
    - Google Analytics (for keeping track of restaurant page traffic)
<br/>

Google reCaptcha
```
Please ask a member of the Find Dining team (that can login with info@finddining.ca)
to add you as an owner of the project
```
- https://www.google.com/recaptcha/admin/
- 3 reCaptcha keys being used:
    - sd-frontend-v2
    - sd-prod-v2
    - sd-test-v2
- Demo for adding Google reCaptcha2 to Angular
    - https://enngage.github.io/ngx-captcha/recaptcha2
    - Source code of demo: https://github.com/Enngage/ngx-captcha/blob/master/demo/src/re-captcha-2-demo.component.ts

<br/>

MapBox
- https://www.mapbox.com/
- The access tokens are accessible by login with email info@finddining.ca

<br/>

Dockerhub Organization: finddiningutsc
```
You can view the latest image tags of docker images that were built and pushed by
either the Github workflow or yourself
```
  - Repositories
    - _finddiningutsc/test_
    - _finddiningutsc/uat_
    - _finddiningutsc/prod_

<br/>

## AODA
We must comply AODA for Angular app. Must achieve level AA of WCAG 2.0

https://www.ontario.ca/page/how-make-websites-accessible

Some useful tools:
- Accessibility Checker:
    - AccessibilityTestFree https://www.accessibilitytestfree.com/
    - WAVE https://wave.webaim.org/
- Contrast Checker:
    - https://webaim.org/resources/contrastchecker/
- Screen Reader:
    - Google Extension https://chrome.google.com/webstore/detail/screen-reader/kgejglhpjiefppelpmljglcjbhoiplfn?hl=en
    - JAWS https://support.freedomscientific.com/Downloads/JAWS

<br />

## Deployment
Github Actions will run the deployment pipeline upon push to one of the three environment branches ``` test, uat, prod ```.

The respective workflow file: ``` deploy.yml ``` is located inside of ``` .github/workflows ``` folder on each of the 3 branches.

### Pushing a new change
Push your changes to master branch.
```
$ git commit -m {{ your_message }}
$ git push
```
Checkout the environment branch and merge. Fix any conflicts.
```
$ git checkout {{ environment }}
$ git merge master
```
Commit and push the changes.
```
$ git push
```
The actions workflow will take ~10 minutes to complete. Then wait an additional ~5 minutes for watchtower to rebuild the docker containers. You can then visit the updated environment site.
  
<br/>

### Files required for deployment
Django
- _settings.py_ in backend/server
- _wsgi.py_ in backend/server

Angular
- _environment.\{{ environment }}.ts_ in client-server/src/environments
  - ``` {{ environment }} can be 'test', 'uat', or 'prod' ```
- _nginx.conf_ in client-server/nginx
- _server.crt_ in client-server/ssl
- _server.key_ in client-server/ssl
  - The .crt and .key files are empty but are required to be present for the Github Actions workflow to execute properly

Docker
- _Dockerfile_ in server
- _Dockerfile_ in client-server
- _docker-compose.yml_ in Find-Dining-Revamp