####################
# Web server stage #
####################
FROM node:latest AS web_server

#Set working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY . /usr/local/app/

# Install all the dependencies
RUN npm install

# Generate the build of the application
RUN npm run build

FROM nginx:1.10.3-alpine
COPY --from=web_server /usr/local/app/dist/runtime /usr/share/nginx/html
EXPOSE 80

