# Project 6: Brevet time calculator service

A simple REST API used to expose the information stored in the Mongo database.

## Functionality 

After downloading the repo, the user may build the required environment by navigating 
to the directiory containing the docker-compose file in the command line, and typing
`docker-compose up`. Once the evironment is running, the user may use the following
functionalities to run the application:

By visiting "http://<host:5002>/" the user may fill the Brevet database with controls. 
Then, to use the RESTful api, the user can visit "http://<host:5000>/" for a simple 
consumer program to return requested information. Alternatively, the user can also
visit "http://<host:5001>/query/format", where query is either "listAll", 
"listOpenOnly", or "listCloseOnly", and format is either "json" or "csv". Be aware: 
the "csv" request will return a .csv file! Lastly, if the user desires, they can 
add the string "?top=integer" to the request, where integer is a positive int 
between 1 and 20 (inclusive), to limit the number of query responses returned. 
