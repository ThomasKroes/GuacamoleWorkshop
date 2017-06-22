# Advanced Guacamole tutorial
*You are encouraged to first complete the [intermediate exercise](../intermediate/exercise.md) before diving into the advanced exercise.*  

The goal of this exercise is to build a more advanced web service by using Guacamole's REST api. We are going to build a simple website that allows an end user to interact with a chosen 3D mesh model using Blender. To this end, we implement a rudimentary Flask web server that:
* Creates Blender containers when 
* Communicates with Guacamole through REST to manage connections
* Provides a portal view for selecting a mesh model

**Note: This exercise will also be run locally on your system using Docker containers. Exposing the service to the outside world is beyond the scope of this exercise (support for this can be provided off-line).**

# Web service anatomy
The [Docker Compose](https://docs.docker.com/compose/) file located [here](source/docker-compose.yml) defines the required services and how they are linked:

```yml
version: '2'

services:
  gw_guacd:
    image: glyptodon/guacd:0.9.9
    container_name: gw.advanced.guacd

  gw_guacdb:
    image: gw_guacdb
    container_name: gw.advanced.mysql
    environment:
      MYSQL_USER: root
      MYSQL_ROOT_PASSWORD: demo
      MYSQL_DATABASE: guacamole

  gw_guac:
    image: glyptodon/guacamole:0.9.9
    container_name: gw.advanced.guac
    depends_on:
      - gw_guacd
      - gw_guacdb
    environment:
      MYSQL_HOSTNAME: gw_guacdb
      MYSQL_DATABASE: guacamole
      MYSQL_USER: root
      MYSQL_PASSWORD: demo
      GUACD_PORT_4822_TCP_ADDR: gw_guacd
      GUACD_PORT_4822_TCP_PORT: 4822

  gw_proxy:
    build: images/gw_proxy
    container_name: gw.advanced.proxy
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
    depends_on:
      - gw_guac
      - gw_flask
    networks:
      - default
    ports:
      - 80:80

  gw_flask:
    build: images/gw_flask
    container_name: gw.advanced.flask
    depends_on:
      - gw_guac
    volumes:
      - ./images/gw_flask:/flask:ro
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - default
```
In the [intermediate](../intermediate/exercise.md) 

This web service consists of the following parts:  
1. **gw_guacd**  
The Guacamole Daemon container that connects with remote desktops over any arbitrary protocol
2. **gw_guacdb**  
The Database container with Guacamole schema as produced earlier in the [prerequisites](../prerequisites/exercise.md)
3. **gw_guac**  
The Guacamole server container. It connects to the Guacamole daemon container (*gw_guacd*) and the Database container (*gw_guacdb*)
4. **gw_proxy**  
An NGINX reverse proxy for routing traffic to the appropriate container. In this web service we have a container for our model loader front-end (*gw_flask*) and a Guacamole container for establishing the remote desktop connection (*gw_guac*). As you can see in the [nginx configuration file](source/images/gw_proxy/nginx.conf), traffic from `http://localhost/guacamole` is directed to the Guacamole server container `proxy_pass http://gw_guac:8080/guacamole/;`. Traffic from `http://localhost/flask` is directed to the Flask webserver container `proxy_pass http://gw_flask/;`.
5. **gw_flask**  
The Flask webserver that provides a front-end where users can choose a Blender scene and view it in the browser. Under the hood, it creates and starts Blender containers (as created in the [prerequisites](../prerequisites/exercise.md)). Furthermore, it automatically creates and configures connections to those Blender containers using Guacamole's REST api. This container is based on the [gw_flask image](#flask-web-server).

## Anatomy of the Flask web server
The source code for the Flask application that runs in **gw_flask** is located in [app.py](source/images/gw_flask/app.py).

The Flask server provides a home view located at *http://localhost/flask*:
```python
# Front end
@app.route("/")
def home():
    return current_app.send_static_file("./html/index.html")
```
It serves a static HTML file that allows users to choose from thee sample Blender scenes:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Guacamole workshop - Advanced</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<div class="jumbotron text-center">
  <h1>View Blender scene</h1>
  <p>Click to load Blender sample scene</p>
    <div>
        <button type="button" class="btn btn-primary" onclick="window.location.href='/flask/view?blender_file=shopping_cart.blend'">Shopping cart</button>
        <button type="button" class="btn btn-primary" onclick="window.location.href='/flask/view?blender_file=fire_extinguisher.blend'">Fire extinguisher</button>
        <button type="button" class="btn btn-primary" onclick="window.location.href='/flask/view?blender_file=watering_can.blend'">Watering can</button>
    </div>
</div>
</body>
</html>
```




