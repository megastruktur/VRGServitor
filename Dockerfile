FROM python:latest
LABEL Maintainer="megastruktur"

WORKDIR /app

COPY . /app

# Set env variables from Github Secrets
RUN --mount=type=secret,id=GOOGLE_API_KEY \
    --mount=type=secret,id=SHEET_ID \
    --mount=type=secret,id=GROUP_CHAT_ID \
    --mount=type=secret,id=BOT_TOKEN \
    --mount=type=secret,id=LOCALE \
      echo $GOOGLE_API_KEY \
      echo $SHEET_ID \
      echo $GROUP_CHAT_ID \
      echo $BOT_TOKEN \
      echo $LOCALE \
      echo $GOOGLE_API_KEY >> /app/.env \
      echo $SHEET_ID >> /app/.env \
      echo $GROUP_CHAT_ID >> /app/.env \
      echo $BOT_TOKEN >> /app/.env \
      echo $LOCALE >> /app/.env

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN pip install -r /app/requirements.txt
#CMD ["python", "main.py"]