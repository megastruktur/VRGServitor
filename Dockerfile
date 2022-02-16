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
    --mount=type=secret,id=SERVICE_ACCOUNT_SECRET_JSON_B64 \
      export GOOGLE_API_KEY=$(cat /run/secrets/GOOGLE_API_KEY) && \
      echo "GOOGLE_API_KEY=$GOOGLE_API_KEY" >> /app/.env && \
      export SHEET_ID=$(cat /run/secrets/SHEET_ID) && \
      echo "SHEET_ID=$SHEET_ID" >> /app/.env && \
      export GROUP_CHAT_ID=$(cat /run/secrets/GROUP_CHAT_ID) && \
      echo "GROUP_CHAT_ID=$GROUP_CHAT_ID" >> /app/.env && \
      export BOT_TOKEN=$(cat /run/secrets/BOT_TOKEN) && \
      echo "BOT_TOKEN=$BOT_TOKEN" >> /app/.env && \
      export LOCALE=$(cat /run/secrets/LOCALE) && \
      echo "LOCALE=$LOCALE" >> /app/.env && \
      cat /run/secrets/SERVICE_ACCOUNT_SECRET_JSON_B64 | base64 -d > /app/service_account_secret.json

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN pip install -r /app/requirements.txt
CMD ["python", "main.py"]