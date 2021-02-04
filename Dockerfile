FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN apt-get install -y wget ca-certificates gnupg2
RUN apt-get install -y postgresql postgresql-contrib
RUN apt-get install -y gcc libc-dev musl-dev build-essential python-psycopg2
COPY ./requirements.txt /requirements.txt
RUN apt install -y zlib1g-dev libjpeg-dev libpq-dev binutils libproj-dev gdal-bin libgdal-dev g++
RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -p for subdirectories
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN useradd user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user