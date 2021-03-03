# Base Image
FROM python:3.8.3

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

ARG DEBUG
ARG SECRET_KEY
ARG DB_ENGINE
ARG DB_NAME
ARG DB_HOST
ARG DB_USER
ARG DB_PASS
ARG GMAIL_API_CLIENT_ID
ARG GMAIL_API_CLIENT_SECRET
ARG GMAIL_API_REFRESH_TOKEN

ENV DEBUG=${DEBUG}
ENV SECRET_KEY=${SECRET_KEY}
ENV DB_ENGINE=${DB_ENGINE}
ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}
ENV DB_PASS=${DB_PASS}
ENV GMAIL_API_CLIENT_ID=${GMAIL_API_CLIENT_ID}
ENV GMAIL_API_CLIENT_SECRET=${GMAIL_API_CLIENT_SECRET}
ENV GMAIL_API_REFRESH_TOKEN=${GMAIL_API_REFRESH_TOKEN}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pipenv && pip3 install -r requirements.txt

# Install project dependencies
RUN pipenv install --skip-lock --system --dev

EXPOSE 8000
CMD python manage.py migrate && uwsgi --socket :8000 --module server.wsgi:application