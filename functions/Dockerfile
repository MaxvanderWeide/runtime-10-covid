FROM python:3 AS cronjob
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app

COPY ping.py /app
COPY fetch_data /app/fetch_data
COPY create_model /app/create_model

RUN pip install -r create_model/requirements.txt
RUN pip install -r fetch_data/requirements.txt
RUN touch cron_logger.log

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
