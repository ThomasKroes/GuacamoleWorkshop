# Prerequisites
Before we can begin with the actual exercises, please make sure that you:
* Have a recent version of [Docker](https://www.docker.com/) installed
* Have a Python distribution such as [Anaconda](https://www.continuum.io/downloads) installed on your system
* Created a [Guacamole MySQL Docker image](#Guacamole-MySQL-Docker-image) (used throughout the exercises)

## Guacamole MySQL Docker image
Throughout this workshop, we make use of a custom [MySQL Docker Image](https://hub.docker.com/_/mysql/) that provides the proper schema such that Guacamole can store information. 

*More information on supported Guacamole Database backends can be found [here](https://github.com/glyptodon/guacamole-docker).*  

Follow the steps below to create the image:
1. Open a terminal and navigate to {clone_dir}/prerequisites/guacdb/.  
This directory contains two files:  
[Dockerfile](guacdb/Dockerfile) for building the Docker image  
[initdb.sql](guacdb/initdb.sql) for injecting the SQL schema when the image is created
2. Execute `docker build . -t guacdb`  
This builds the Guacamole database image and stores it in the local Docker registry. In the next exercises you will see references to this image.

Now that the database image has been built, you can continue with the [intermediate](intermediate/exercise.md) or [advanced](advanced/exercise.md) exercises.
