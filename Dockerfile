####################
# Web server stage #
####################
FROM node:latest AS web_server

#Set working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY /front-end/ /usr/local/app/

# Install all the dependencies
RUN npm install

# Generate the build of the application
RUN npm run build

FROM nginx:1.10.3-alpine
COPY --from=web_server /usr/local/app/dist/runtime /usr/share/nginx/html
EXPOSE 4200

####################
# API stage        #
####################
FROM python:3 AS flask_api
COPY /back-end /back-end
RUN pip install -r /back-end/api_server/requirements.txt
ENV PYTHONPATH='/back-end/api_server'
ENTRYPOINT ["python", "/back-end/api_server/openapi_server/__main__.py"]

#FROM python:3
#COPY /storage_mock /storage_mock
#ENTRYPOINT ["python", "/storage_mock/storage_client.py"]

####################
# Cronjob stage    #
####################
FROM python:3 AS cronjob
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app

COPY functions/ping.py /app
COPY functions/fetch_data /app/fetch_data
COPY functions/create_model /app/create_model

RUN pip install -r create_model/requirements.txt
RUN pip install -r fetch_data/requirements.txt
RUN touch cron_logger.log

COPY functions/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

