# Runtime-10-covid

SARS-CoV-2, Covid-19 dashboard created for the Data Science and Society Master's course at Utrecht University.

Created by Team 10, Runtime Error

Made by ***Max van der Weide**, **Milo Voorhout**, **Björn Koemans*** and ***Samtag Prakke***.

## Table of Contents

* [Why Docker](#why-docker)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Containers & Images](#containers)
* [Run Dashboard](#run-dashboard)


## Why Docker
"With Docker, developers can build any app in any language using any toolchain. “Dockerized” apps are completely portable and can run anywhere - colleagues’ OS X and Windows laptops, QA servers running Ubuntu in the cloud, and production data center VMs running Red Hat.

Developers can get going quickly by starting with one of the 13,000+ apps available on Docker Hub. Docker manages and tracks changes and dependencies, making it easier for sysadmins to understand how the apps that developers build work. And with Docker Hub, developers can automate their build pipeline and share artifacts with collaborators through public or private repositories.

Docker helps developers build and ship higher-quality applications, faster." -- [What is Docker](https://www.docker.com/what-docker#copy1)

## Prerequisites
The dashboard uses [Angular](https://angular.io/) for its front-end and [Flask](https://flask.palletsprojects.com/en/2.2.x/) for its back-end. As and end user you don't need to install any of these but as developer you do. To see prerequisites for developer go to [Developers](#Developers). 


### Linux

The 3.10.x kernel is [the minimum requirement](https://docs.docker.com/engine/installation/binaries/#check-kernel-dependencies) for Docker.

### MacOS

MacOS 10.15 “Catalina” or newer is required.

### Windows

Windows 11 64-bit: Home or Pro version 21H2 or higher, or Enterprise or Education version 21H2 or higher.

Windows 10 64-bit: Home or Pro 21H1 (build 19043) or higher, or Enterprise or Education 20H2 (build 19042) or higher.

Hyper-V must be enabled in BIOS

VT-D must also be enabled if available (Intel Processors).

### Windows Server

Windows Server 2016 is the minimum version required to install docker and docker-compose. Limitations exist on this version, such as multiple virtual networks and Linux containers. Windows Server 2019 and later are recommended.

## Containers

[Docker Container](https://www.edureka.co/blog/what-is-docker-container) is a standardized unit which can be created on the fly to deploy a particular application or environment. This dashboard is separated into three different docker containers build opun three different docker images. The three containers in question are:

* Web = front-end aka Angular project.
* API = back-end aka Flask project.
* Cron = a container containing a data fetcher and model creation.

Each of these containers has their own Dockerfile (Docker image). Images are just [templates for docker containers](https://docs.docker.com/engine/understanding-docker/#how-does-a-docker-image-work). These docker images can be found at:

* Web = `/front-end/Dockerfile`
* API = `/back-end/Dockerfile`
* Cron = `/funtions/Dockerfile`

## Run Dashboard

Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration. To learn more about all the features of Compose, see the [list of features](https://docs.docker.com/compose/overview/#features).

To **run** this dashboard you can simply run the following command: ``` docker-compose up```. After running the command, the dashboard will be build and you will be able to connect. For the front-end you can connect to `http://localhost:4200` and for the back-end you can connect to `http://localhost:8080`.


