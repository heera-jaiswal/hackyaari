from run import db

class Bus(db.Model):
	__tablename__="bus"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(120))

	def __init__(self):
		pass

	def __repr__(self):
		return '<Name %r>' % self.name

class BusState(db.Model):
	"""docstring for BusState"""
	__tablename__="bus_state"
	id = db.Column(db.Integer, primary_key=True)
	bus_id = db.Column(db.Integer)
	x = db.Column(db.Integer)
	y = db.Column(db.Integer)
	direction_x = db.Column(db.Integer)
	direction_y = db.Column(db.Integer)
	pax_collected = db.Column(db.Integer)
	iter_no = db.Column(db.Integer)	

	def __repr__(self):
		return '<ID = %d>' % self.id
		
