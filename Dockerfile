FROM python:latest
LABEL Maintainer="megastruktur"

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN pip install -r /app/requirements.txt
CMD ["python", "main.py"]