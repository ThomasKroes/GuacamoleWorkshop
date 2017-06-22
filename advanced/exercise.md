# Advanced Guacamole tutorial
*You are encouraged to first complete the [intermediate exercise](../intermediate/exercise.md) before diving into the advanced exercise.*  

The goal of this exercise is to build a more advanced web service by using Guacamole's REST api. We are going to build a simple website that allows an end user to interact with a chosen 3D mesh model using Blender. To this end, we implement a rudimentary Flask web server that:
* Manages Blender containers 
* Communicates with Guacamole through REST to manage connections
* Provides a portal for viewing a Blender scene

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
When a Blender scene is picked, the user is redirected to:

```python
@app.route("/view", methods=["GET"])
def view():
    blender_file = str(request.args.get("blender_file"))

    # Create Blender Docker container
    container_name = create_blender_container(blender_file)

    # Hack to ensure the container is fully operational when we start streaming
    time.sleep(2.5)

    # Redirect to Guacamole Blender connection
    return redirect(create_guacamole_connection(container_name))
```

This part defines a Flask view for viewing a particular Blender scene. First, the Blender file that needs to be displayed is extracted from the request arguments. Once the Blender file is known, a Blender container is created and started. Then, a new Guacamole connection to the previously generated Blender container is made, and the user is redirect to the page that connects to the Blender container with Guacamole. Let's look into more detail how the container is created:

```python
# Create Blender Docker container
def create_blender_container(blender_file):

    # Create session id
    session_id = str(shortuuid.uuid())

    # Compose container name
    container_name = "blender_" + session_id

    # Container environment variables
    environment = ["BLENDER_FILE=" + blender_file]

    # Blender image name in the local Docker registry
    image_name = "gw_blender"

    # Join the default network
    networking_config = docker_client.create_networking_config(
        {"source_default": docker_client.create_endpoint_config()})

    container = docker_client.create_container(image=image_name,
                                               name=container_name,
                                               environment=environment,
                                               networking_config=networking_config,
                                               cpuset="0-3")

    docker_client.start(container=container.get('Id'))

    return container_name
```

First, a unique container name is generated and, in order to avoid name conflicts. Next, the BLENDER_FILE environment variable is set to the value that the user specified. This way, when the Blender container starts up it will load the appropriate Blender file. The Blender container also has to join the default network in order to allow for communication between the Guacamole server and Blender. What remains is to create and start the container. The function returns the container ID, which is used later as a reference in Guacamole.

Once the Blender container is created and started, a new connection has to be made in Guacamole:
```python
# Add connection to Blender Docker container using Guacamole's REST api
def create_guacamole_connection(container_name):

    # Obtain authentication token
    guacamole_token = guacamole_authenticate()

    if not guacamole_token:
        return "Unable to authenticate"

    # Connection information
    connection = dict()

    # Basic connection parameters
    connection["name"]              = container_name
    connection["parentIdentifier"]  = "ROOT"
    connection["protocol"]          = "vnc"

    # Create attributes dictionary
    connection["attributes"]  = dict()

    # And populate it with the proper values
    connection["attributes"]["max-connections"]             = "10"
    connection["attributes"]["max-connections-per-user"]    = "10"

    # Create protocol specific parameters dictionary
    connection["parameters"] = dict()

    # And populate it with the proper vnc parameters
    connection["parameters"]["hostname"]    = container_name
    connection["parameters"]["port"]        = "5900"
    connection["parameters"]["read-only"]   = False
    connection["parameters"]["color-depth"] = 24

    # Add the new connection using the guacamole rest api
    response = requests.post(guacamole_url + "api/data/mysql/connections", data=json.dumps(connection), params=guacamole_token, headers={"Content-type": "application/json"})

    # Get response content
    content = json.loads(response.content)

    # Try obtain the connection id from the http request response
    if "identifier" in content:
        connection_id = content["identifier"]
    else:
        return "Unable to add connection: " + str(response.content)

    client_string = str(connection_id) + "\0c\0mysql"
    client_base64 = base64.b64encode(client_string)

    return "http://localhost/guacamole/#/client/" + client_base64 + "?username=guacadmin&password=guacadmin"
```
   


