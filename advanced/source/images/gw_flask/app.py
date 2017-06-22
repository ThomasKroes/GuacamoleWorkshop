import time
import shortuuid
import requests
import json
import base64

from docker import Client
from flask import Flask, redirect, request, current_app

app = Flask(__name__)

# Docker python bindings for managing containers
docker_client = Client(base_url='unix://var/run/docker.sock')

# Traffic to Guacamole is proxied through gw_proxy
guacamole_url = "http://gw_proxy/guacamole/"


# Obtain an authentication token from the Guacamole server (token is used in REST calls)
def guacamole_authenticate():
    global guacamole_token

    # Post request to obtain token
    response = requests.post(guacamole_url + "api/tokens", auth=('guacadmin', 'guacadmin'))

    # Convert response content to python dictionary
    content = json.loads(response.content)

    # Check if we successfully logged into the guacamole rest server
    if "authToken" in content:
        return {'token': json.loads(response.content)["authToken"]}
    else:
        return None


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

@app.route("/view", methods=["GET"])
def view():
    blender_file = str(request.args.get("blender_file"))

    # Create Blender Docker container
    container_name = create_blender_container(blender_file)

    # Hack to ensure the container is fully operational when we start streaming
    time.sleep(2.5)

    # Redirect to Guacamole Blender connection
    return redirect(create_guacamole_connection(container_name))


# Front end
@app.route("/")
def home():
    return current_app.send_static_file("./html/index.html")


if __name__ == '__main__':

    # Run the Flask application with debugging
    app.run(host="0.0.0.0", port=80, debug=True, use_debugger=True)
