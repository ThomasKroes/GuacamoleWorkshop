# Intermediate exercise
The goal of this exercise is to make Blender available in the browser using Guacamole. We will start our webservice using [Docker Compose](https://docs.docker.com/compose/) and configure Guacamole so that we can use Blender within the browser.

**Note: In the interest of time, this exercise will be run locally on your system using Docker containers. Exposing the service to the outside world is beyond the scope of this exercise (of course guidance can be provided off-line).**

Please make sure you have all the necessary [prerequisites](../prerequisites/exercise.md) before going any further.

## Step 1: Starting the Guacamole web service
1. Open a terminal and navigate to `{clone_url}/intermediate/source`
2. Run `docker-compose up`

## Step 2: Configure Guacamole
1. In a browser of choice, navigate to [localhost](http://localhost)
2. You will be presented with a login screen
[login](images/login.png)
, enter the following credentials: guacadmin/guacadmin
3. 
