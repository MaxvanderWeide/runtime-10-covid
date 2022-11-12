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
EXPOSE 80

FROM python:3
COPY /storage_mock /storage_mock
ENTRYPOINT ["python", "/storage_mock/storage_client.py"]

FROM python:3
COPY /back-end /back-end
RUN pip install -r /back-end/api_server/requirements.txt
ENV PYTHONPATH='/back-end/api_server'
ENTRYPOINT ["python", "/back-end/api_server/openapi_server/__main__.py"]


