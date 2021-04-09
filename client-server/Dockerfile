#############
### build ###
#############

# base image
FROM node:12.16.2 as build

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@9.1.9

# add app
COPY . /app

# run tests
# RUN ng test --watch=false
# RUN ng e2e --port 4202

# generate build
ARG CONFIG
RUN ng build --configuration=${CONFIG} --output-path=dist

############
### deploy ###
############

# base image
FROM nginx:1.16.0-alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

# copy django admin static files nginx/html directory
COPY static /usr/share/nginx/html/static

COPY ssl/server.crt /etc/nginx/certs/server.crt
COPY ssl/server.key /etc/nginx/certs/server.key

# copy artifact build from the 'build environment'
COPY --from=build /app/dist /usr/share/nginx/html

ARG HTTP_PORT
ARG HTTPS_PORT
# expose port 80 or 8080 listening for http
EXPOSE ${HTTP_PORT}
#expose port 443 or 8443 listening for https
EXPOSE ${HTTPS_PORT}

# run nginx
CMD ["nginx", "-g", "daemon off;"]