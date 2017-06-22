
import time
import shortuuid
import requests
import json
import base64
import datetime
import dateutil.parser

from docker import Client
from flask import Flask, render_template, redirect, url_for, request

app 				= Flask(__name__)
docker_client 		= Client(base_url='unix://var/run/docker.sock')
guacamole_url		= "localhost/guacamole/"
guacamole_token 	= None
json_header			= { "Content-type" : "application/json" }

# def guacamole_authenticate():
# 	global guacamole_token
#
# 	# No need to update the guacamole token if we have a valid one
# 	# if guacamole_token is not None:
# 	# 	return
#
# 	# Try to log into the guacamole rest server
# 	response = requests.post(guacamole_url + "api/tokens", data={ "username" : "guacadmin", "password" : "guacadmin" }, headers={ "Content-type": "application/x-www-form-urlencoded" })
#
# 	# Convert response content to python dictionary
# 	content = json.loads(response.content)
#
# 	# Check if we successfully logged into the guacamole rest server
# 	if "authToken" in content:
# 		guacamole_token = {'token': json.loads(response.content)["authToken"]}
#
# @app.route('/run', methods=['GET'])
# def run():
# 	# Get pipeline name and configuration
# 	pipeline_name 	= str(request.args.get("name"))
# 	pipeline_config = str(request.args.get("config"))
#
# 	session_id 			= str(request.args.get("session_id"))		# Session id (if set join session, otherwise create a new one)
# 	container_prefix	= "bbmri.demo.viewer."						#
# 	container_name		= container_prefix
# 	connection_id		= str(request.args.get("connection_id"))
#
# 	clear_old()
# 	# Redirect to guacamole if a connection id is present
# 	# if connection_id == "None":
# 	#  	pass
# 	# else:
# 	#  	client = base64.b64encode(str(connection_id) + "cmysql")
# 	# 	return redirect("http://bbmri.ewi.tudelft.nl/guacamole/#/client/" + client)#guacamole_url + "#/c/" + str(connection_id) + "?username=guacadmin&password=guacadmin")
#
# 	if session_id == "None":
# 		# No session specified
# 		# create a new session and container
#
# 		# Create session id
# 		session_id = str(shortuuid.uuid())
#
# 		# Compose container name
# 		container_name = container_name + session_id
#
# 		# Container environment variables
# 		environment = ["PIPELINE_NAME=" + pipeline_name, "PIPELINE_CONFIG=" + pipeline_config]
#
# 		# Map volume for the connectomizer app
# 		host_config = docker_client.create_host_config(binds=	{
#  																	'/home/thomas/workspaces/examples' : { 'bind': '/examples', 'mode': 'rw' },
# 																	'/home/thomas/workspaces/bbmri' : { 'bind': '/bbmri', 'mode': 'rw' }
# 																})
# 		image_name="bbmri.registry.ewi.tudelft.nl/sandbox/viewer"
#
# 		# Make sure we have the latest version of the viewer
# 		docker_client.pull(image_name)
#
# 		networking_config = docker_client.create_networking_config({ 'bbmridemoewitudelftnl_default':  docker_client.create_endpoint_config()
# })
#
# 		container = docker_client.create_container(	image=image_name,
# 													name=container_name,
# 													environment=environment,
# 													volumes=["/examples", "/bbmri"],
# 													host_config=host_config, networking_config=networking_config,
# 													cpuset="0-9")
#
#
# 		docker_client.start(container=container.get('Id'))
#
# 		# Hack to ensure the container is fully operational when we start streaming
# 		time.sleep(2.5)
#
#
#
# 		#docker_client.connect_container_to_network(container.get('Id'), "bbmridemoewitudelftnl_internal")
# 		#docker_client.connect_container_to_network(container.get('Id'), "bbmridemoewitudelftnl_default")
# 	# else:
# 		# Session specified
# 		# Find existing container
#
# 	# Login to guacamole
# 	guacamole_authenticate()
#
# 	# Obtain container info so that we can retrieve the ip address
# 	container_info = docker_client.inspect_container(container_name)
#
# 	# Retrieve ip address from container info
# 	ip_address = container_info["NetworkSettings"]["IPAddress"]
#
# 	# Connection information
# 	connection = dict()
#
# 	# Basic connection parameters
# 	connection["name"] 				= container_name
# 	connection["parentIdentifier"] 	= "ROOT"
# 	connection["protocol"] 			= "vnc"
#
# 	# Create attributes dictionary
# 	connection["attributes"] = dict()
#
# 	# And populate it with the proper values
# 	connection["attributes"]["max-connections"] 			= "100"
# 	connection["attributes"]["max-connections-per-user"] 	= "100"
#
# 	# Create 7protocol specific parameters dictionary
# 	connection["parameters"] = dict()
#
# 	# And populate it with the proper vnc parameters
# 	# with connection["parameters"] as parameters:
# 	connection["parameters"]["hostname"] 	= container_name
# #str(ip_address)
# 	connection["parameters"]["port"] 		= "5900"
# 	connection["parameters"]["password"] 	= "vncpassword"
# 	connection["parameters"]["read-only"] 	= False
# 	connection["parameters"]["color-depth"] = 24
#
# 	# Add the new connection using the guacamole rest api
# 	response=requests.post(guacamole_url + "api/data/mysql/connections", data=json.dumps(connection), params=guacamole_token, headers=json_header)
#
# 	# return str(guacamole_token)
#
# 	# Get response content
# 	content = json.loads(response.content)
#
# 	# Try obtain the connection is from the http request reponse
# 	if "identifier" in content:
# 		connection_id = content["identifier"]
# 	else:
# 		return "Unable to add connection: " + str(response.content)
#
# 	client_string = str(connection_id) + "\0c\0mysql"
# 	client_base64 = base64.b64encode(client_string)
#
# 	return redirect(guacamole_url + "#/client/" + client_base64 + "?username=guacadmin&password=guacadmin")  # guacamole_url + "#/c/" + str(connection_id) + "?username=guacadmin&password=guacadmin")

# @app.route('/clear_old')
# def clear_old():
#
# 	# Log into guacamole
# 	guacamole_authenticate()
#
# 	# Get a list of containers
# 	containers = docker_client.containers()
#
# 	# List of obsolete (idle) viewer containers eligible for deletion
# 	obsolete_container_names = []
#
# 	# Elapsed time till now
# 	now = datetime.datetime.now()
#
# 	# Inspect every container and remove if necessary
# 	for container in containers:
# 		# Inspect the container
# 		container_name = container["Names"][0]
# 		container_info = docker_client.inspect_container(container_name)
#
# 		# Potentially remove viewer
# 		if container_name.startswith("/bbmri.demo.viewer."):
# 			# Compute how long the viewer container has been up
# 			started_at			= dateutil.parser.parse(container_info[u'State'][u'StartedAt']).replace(tzinfo=None)
# 			container_duration	= now - started_at
#
# 			# Remove the viewer container if it has been up more than one hour
# 			if container_duration.seconds > 1800:
# 				#1800:
# 				# Stop the container, and remove it from the registry
# 				docker_client.kill(container["Id"])
# 				docker_client.remove_container(container["Id"])
#
# 				# Queue the container for deletion from guacamole
# 				obsolete_container_names.append(container_name)
#
#
# 	# ToDo: Also remove connection entries from guacamole
# 	#for connection_id in range(100):
# 	#	requests.delete(guacamole_url + "api/data/mysql/connections/" + str(connection_id), params=guacamole_token, headers=json_header)
#
# 	return "Removed: %s" % str(obsolete_container_names)

# @app.route('/clear_all')
# def clear_all():
# 	removed = list()
#
# 	# Get a list of containers
# 	containers = docker_client.containers()
#
# 	# Inspect every container and remove if necessary
# 	for container in containers:
# 		# Inspect the container
# 		container_name = container["Names"][0]
# 		container_info = docker_client.inspect_container(container_name)
#
# 		# Remove viewer
# 		if container_name.startswith("/bbmri.demo.viewer."):
# 			docker_client.kill(container["Id"])
# 			docker_client.remove_container(container["Id"])
#
# 			removed.append(container_name)
#
# 	return "Removed containers: " + str(removed)

@app.route('/')
def index():

	return current_app.send_static_file('/html/index.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80, debug=True, use_debugger=True)
	#app.run(host="0.0.0.0", port=80)
