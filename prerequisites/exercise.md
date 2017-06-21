# Prerequisites
Before we can begin with the actual exercises, please make sure that you:
* Have a recent version of [Docker](https://www.docker.com/) installed
* Have a Python distribution such as [Anaconda](https://www.continuum.io/downloads) installed on your system
* Created a [Guacamole MySQL Docker image](#guacamole-mysql-image)
* Created a [Desktop Docker image](#desktop-image)
* Created a [Blender Docker image](#blender-desktop-image) 

If done so, you can continue with the [intermediate](../intermediate/exercise.md) or [advanced](../advanced/exercise.md) exercises.

## Guacamole MySQL image
Throughout this workshop, we make use of a custom [MySQL Docker Image](https://hub.docker.com/_/mysql/) that provides the proper schema such that Guacamole can store information. 

*More information on supported Guacamole Database backends can be found [here](https://github.com/glyptodon/guacamole-docker).*  

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/guacdb/`.  
This directory contains the following files:  
[Dockerfile](guacdb/Dockerfile) for building the image  
[initdb.sql](guacdb/initdb.sql) for injecting the SQL schema at image creation time
2. Execute `docker build . -t guacdb`  
This builds the Guacamole database Docker image and stores it in the local Docker registry as `guacdb`.  

*In the exercises you will see references to this image in docker-compose.yml files.*

## Desktop image
In the following exercises, we will run Blender in a Docker container based on a desktop Docker image. This desktop image combines [XFCE](https://xfce.org/) with [XVFB](https://en.wikipedia.org/wiki/Xvfb), so that the desktop containers can be run headless. Furthermore it has [VNC](http://www.karlrunge.com/x11vnc/) for remote control by Guacamole.  

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/desktop/`.  
This directory contains the following files:  
[Dockerfile](desktop/Dockerfile) for building the image.  
[startup.sh](desktop/startup.sh) is the main entry point for the Docker container  
[supervisord.conf](desktop/supervisord.conf) configures the process manager (e.g. XVFB, X11VNC & SSH)
2. Execute `docker build . -t desktop`  
This builds the desktop Docker image and stores it in the local Docker registry as `desktop`.

## Blender desktop image
The goal of this workshop is to make Blender available in the browser. In order to do so, we create a Blender Docker image which is based on the previously generated [Desktop image](#desktop-image).

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/guacdb/`.  
This directory contains the following files:  
[Dockerfile](guacdb/Dockerfile) for building the image  
[initdb.sql](guacdb/initdb.sql) for injecting the SQL schema when the image is created
2. Execute `docker build . -t guacdb`  
This builds the Blender Docker image and stores it in the local Docker registry.  

*In the exercises you will see references to this image in docker-compose.yml files.*


