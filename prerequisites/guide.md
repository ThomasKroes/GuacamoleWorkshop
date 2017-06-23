# Prerequisites
Before we can begin with the actual exercises, please make sure that you:
* Cloned this repository 
* Have a recent version of [Docker](https://www.docker.com/) installed
* Created a [Guacamole MySQL Docker image](#guacamole-mysql-image)
* Created a [Desktop Docker image](#desktop-image)
* Created a [Blender Docker image](#blender-desktop-image) 

If done so, you can continue with the [intermediate](../intermediate/exercise.md) or [advanced](../advanced/exercise.md) exercises.

## Guacamole MySQL image
Throughout this workshop, we make use of a custom [MySQL Docker Image](https://hub.docker.com/_/mysql/) that provides the proper schema such that Guacamole can store information. 

*More information on supported Guacamole Database backends can be found [here](https://github.com/glyptodon/guacamole-docker).*  

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/gw_guacdb/`.  
This directory contains the following file(s):  
[Dockerfile](gw_guacdb/Dockerfile) for building the image  
[initdb.sql](gw_guacdb/initdb.sql) for injecting the SQL schema at image creation time
2. Execute `docker build . -t gw_guacdb`  
This builds the Guacamole database Docker image and stores it in the local Docker registry as **gw_guacdb**.  

*In the exercises you will see references to this image in docker-compose.yml files.*

## Desktop image
In the following exercises, we will run Blender in a Docker container based on a desktop Docker image. This desktop image combines [XFCE](https://xfce.org/) with [XVFB](https://en.wikipedia.org/wiki/Xvfb), so that the desktop containers can be run headless. Furthermore it has [VNC](http://www.karlrunge.com/x11vnc/) for remote control by Guacamole.  

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/gw_desktop/`.  
This directory contains the following file(s):  
[Dockerfile](gw_desktop/Dockerfile) for building the image  
[startup.sh](gw_desktop/startup.sh) is the main entry point for the Docker container (starts the supervisor daemon)  
[supervisord.conf](gw_desktop/supervisord.conf) configures the process manager and services (e.g. XVFB, X11VNC & SSH)
2. Execute `docker build . -t gw_desktop`  
This builds the desktop Docker image and stores it in the local Docker registry as **gw_desktop**.

## Blender desktop image
The goal of this workshop is to make Blender available in the browser. To this end, we create a Blender Docker image which is based on the previously generated [Desktop image](#desktop-image).

Follow the steps below to create the Docker image:
1. Open a terminal and navigate to `{clone_dir}/prerequisites/gw_blender/`.  
This directory contains the following file(s):  
[blender.desktop](gw_blender/blender.desktop) runs at startup and executes blender.sh  
[blender.sh](gw_blender/blender.sh) starts Blender with the appropriate scene (from environment variable BLENDER_FILE)  
[Dockerfile](gw_blender/Dockerfile) for building the image  
2. Execute `docker build . -t gw_blender`  
This builds the Blender Docker image and stores it in the local Docker registry as **gw_blender**.  

*In the exercises you will see references to this image in docker-compose.yml files.*

You can now continue with the [intermediate](../intermediate/exercise.md) or [advanced](../advanced/exercise.md) exercise.

<!---* Have a Python distribution such as [Anaconda](https://www.continuum.io/downloads) installed on your system-->
