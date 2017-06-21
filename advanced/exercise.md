# Advanced Guacamole tutorial
*You are encouraged to first complete the [intermediate exercise](../intermediate/exercise.md) before diving into the advanced exercise.*  

The goal of this exercise is to build a more advanced web service by using Guacamole's REST api. We are going to build a simple website that allows an end user to interact with a chosen 3D mesh model using Blender. To this end, we implement a rudimentary Flask web server that:
* Communicates with Guacamole through REST to manage users, connections etc.
* Provides a portal view for selecting a mesh model

**Note: This exercise will also be run locally on your system using Docker containers. Exposing the service to the outside world is beyond the scope of this exercise (support for this can be provided off-line).**
