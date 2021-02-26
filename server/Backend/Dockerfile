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

ENV DEBUG=True
ENV SECRET_KEY='dr5xc)!0v+psc731_ps1a!=1tnxci5pm#2rgqhg!&&9qdxds@w'
ENV DB_ENGINE=djongo
ENV DB_NAME=scdining
ENV DB_HOST='mongodb+srv://user:X7FHovuCvNroNlCZ@scdining.vgvie.mongodb.net/scdining?retryWrites=true&w=majority'
ENV DB_USER=user
ENV DB_PASS=X7FHovuCvNroNlCZ

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