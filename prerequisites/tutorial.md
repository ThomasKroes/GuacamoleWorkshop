# Prerequisites
Before we can begin with the actual excersises, please make sure that you:
* Have a recent version of [Docker](https://www.docker.com/) installed
* Have a Python distribution such as [Anaconda](https://www.continuum.io/downloads) installed on your system
* Created a [Guacamole MySQL Docker image](#Guacamole-MySQL-Docker-image) (used throughout the tutorials)

## Guacamole MySQL Docker image
Throughout this workshop, we use a MySQL Docker Image to store information for Guacamole. To this end, we need to create a MySQL docker image that has all the schemas in place such that the Guacamole Server can use it. Follow the steps below to create the image:
1. Open a terminal and navigate to {clone_dir}/prerequisites/guacdb/.  
This directory contains two files:  
[Dockerfile](guacdb/Dockerfile) for building the Docker image  
[initdb.sql](guacdb/initdb.sql) for injecting the SQL schema when the image is created
2. Execute `docker build . -t guacdb`  
This builds the Guacamole database image and stores it in the local Docker registry.

More information on supported Database backends can be found [here](https://github.com/glyptodon/guacamole-docker).
