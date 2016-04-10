from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

USER_NAME='test'
PASSWORD='test'
SERVER='localhost'
DB_NAME='hackyaari'
app = Flask("HackYaari")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/repo/hackyaari/env/data/hackyaari.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://"+USER_NAME+":"+PASSWORD+"@"+SERVER+"/"+DB_NAME+"?charset=utf8"


db = SQLAlchemy(app)
api = Api(app)

import models
class Map(Resource):
    def get(self,bus_id):        
        return {"state":state}

    def post(self, bus_id, move):
    	#args = parser.parse_args()                
        return {"success":True,"data":{"bus_id":bus_id,"move":move}},200

class Bus(Resource):
	def get(self,bus_id):						
		import core
		bus=core.get_bus(int(bus_id))
		return {"bus_id":bus.id,"bus_name":bus.name}

class Register(Resource):
	def get(self,name,email):						
		import core
		bus = core.create_bus(name,email)
		return {"id":bus.id,"bus":bus.name,"email":bus.email}	

class Command(Resource):
	def get(self,bus_id,command):
		import core
		my_pos,cur_dir,pax_collected = core.run_command(bus_id,command)
		return {"position":my_pos,"direction":cur_dir,"pax_collected":pax_collected}
	
##
## Actually setup the Api resource routing here
##
api.add_resource(Map,'/map/<int:state>/',endpoint='map')
api.add_resource(Bus,'/bus/<int:bus_id>/',endpoint='bus')
api.add_resource(Register,'/register/<string:name>/<string:email>/',endpoint='register')
api.add_resource(Command,'/command/<int:bus_id>/<string:command>/',endpoint='command')



if __name__ == '__main__':
	from engine import init_map_feed
	#init_map_feed()

	app.run(debug=True)