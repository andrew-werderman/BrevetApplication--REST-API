# Brevet RESTful API
# Author: Andrew Werderman

import flask
from flask import (
	Flask, redirect, url_for, request, render_template, Response, jsonify 
	)
from flask_restful import Resource, Api
from pymongo import MongoClient

# Instantiate the app
app = Flask(__name__)
api = Api(app=app, catch_all_404s=True)

# Create Mongo instance
client = MongoClient('mongodb://mongo:27017/')
database = client['brevetdb']

class Home(Resource):
    def get(self):
        return {'Error': "These aren't the droids you are looking for."}

class ListBrevet(Resource):
	def __init__(self):
		self.collection = database['brevet']

	def get(self, items='listAll', resultFormat='json'):
		'''
		  Input:
			items - which items to list: 'listAll' (default), 'listOpenOnly', 'listCloseOnly'
			resultFormat - requested format of response
		  Output:
			array of brevet control open and/or close times
			resultFormat='json' gives an array of dictionaries
			resultFormat='csv' gives an array of arrays
		'''
		top = request.args.get('top')

		# Handle empty brevet
		if self.collection.find().count() == 0:
			return jsonify({'Error': 'Empty Brevet'})

		# Handle unexpected query.
		if (items not in ['listAll', 'listOpenOnly', 'listCloseOnly']) or (resultFormat not in ['json', 'csv']):
			return jsonify({'Error': 'Invalid Query'})

		# Handle whether top is set or not
		if (top == None) or (top == ''):
			controls = self.collection.find()
		else:
			# Handle invalid input for top
			try:
				limit = int(top)
				if(limit <= 0):
					return jsonify({'Error': 'Invalid number of top elements'})
				else:
					controls = self.collection.find(limit=limit) # limits the number of results in find()
			except ValueError:
				return jsonify({'Error': 'Value Error for top'})

		# Populate results with queried output
		if (items == 'listAll'):
			result = ListBrevet.formatResponse(controls, resultFormat, 'open_time', 'close_time')
		elif (items == 'listOpenOnly'):
			result = ListBrevet.formatResponse(controls, resultFormat, 'open_time')
		else: # resultFormat == 'listCloseOnly'
			result = ListBrevet.formatResponse(controls, resultFormat, 'close_time')
		
		if (resultFormat == 'csv'):
			return Response(result, mimetype='text/csv')

		return jsonify(result)


	def formatResponse(brevet, resultFormat, *args):
		'''
		  Input: 
		  	brevet - the db brevet collection instance
		  	resultFormat - the desired output format of the query -- 'json' or 'csv'
		  	*args - the key values of the desired control information -- 'open_time'/'close_time'/etc.
		  Output: 
		  	json - an array of dictionaries of control info
		  	csv - A string formatted to csv
		  Helper function to format the queried resultFormat of controls.
		'''
		json = []
		csv = ''
		if (resultFormat == 'json'):
			for ctrl in brevet:
				jsonDict = {key:ctrl[key] for key in args}
				json.append(jsonDict)
		else:
			csv += str(args[0])
			if (len(args) > 1):
				csv += ', {}\n'.format(args[1])
				for ctrl in brevet:
					csv += '{}, {}\n'.format(ctrl[args[0]], ctrl[args[1]])
			else:
				csv += '\n'
				for ctrl in brevet:
					csv += '{}\n'.format(ctrl[args[0]])

		output = {'json': json, 'csv': csv}
		return output[resultFormat]


# Create routes
api.add_resource(Home, '/')
api.add_resource(ListBrevet, '/<items>/<resultFormat>', endpoint='get')

# Run the application
if __name__ == '__main__':
    app.run(
    	host='0.0.0.0', 
    	port=80, 
    	debug=True,
    	extra_files = './templates/response.html')

