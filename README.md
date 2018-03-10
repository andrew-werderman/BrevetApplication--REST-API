# Project 6: Brevet time calculator service

Simple listing service from project 5 stored in MongoDB database.

## What is in this repository

You have a minimal implementation of Docker compose in DockerRestAPI folder,
using which you can create REST API-based services (as demonstrated in 
class). Refer to the lecture slide "05a-Mongo-Docker-Compose.pdf" (dated 
02/15/2018) for information about how to use Docker compose. 


## Functionality 

By visiting "http://<host:5002>/" the user may fill the Brevet database with controls. 
Then, to use the RESTful api, the user can visit "http://<host:5000>/" for a simple 
consumer program to return requested information. Alternatively, the user can also
visit "http://<host:5001>/query/format", where query is either "listAll", 
"listOpenOnly", or "listCloseOnly", and format is either "json" or "csv". Be aware: 
the "csv" request will return a .csv file! Lastly, if the user desires, they can 
add the string "?top=integer" to the request, where integer is a positive int 
between 1 and 20 (inclusive), to limit the number of query responses returned. 
