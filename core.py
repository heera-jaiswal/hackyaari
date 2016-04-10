from run import db
import models
import engine

def create_bus(name,email):
	bus = models.Bus()
	bus.name=name
	bus.email=email
	db.session.add(bus)
	db.session.commit()
	return bus

def get_bus(bus_id):
	buses = models.Bus.query.filter_by(id=bus_id).all()
	if len(buses)>0:
		return buses[0]
	else:
		raise Exception("Not found !")

def run_command(bus_id,command):
	my_pos="0,0"
	cur_dir="1,0"
	iter_no=0
	command=command.upper()
	if not command in engine.COMMANDS:
		raise Exception("Command not found !")	

	buses = models.Bus.query.filter_by(id=bus_id).all()
	bus=None
	if len(buses)>0:
		bus = buses[0]
	else:
		raise Exception("Bus Not found !")
		
	if engine.COMMANDS[command]==engine.RESET:
		models.BusState.query.filter_by(bus_id=bus.id).delete()
		db.session.commit()
		return my_pos,cur_dir,0

	bus_states = models.BusState.query.filter_by(bus_id=bus.id).order_by(models.BusState.iter_no.desc()).all()	
	
	cur_state=None
	if len(bus_states)>0:
		cur_state=bus_states[0]
		my_pos=str(cur_state.x)+","+str(cur_state.y)
		cur_dir=str(cur_state.direction_x)+","+str(cur_state.direction_y)		
		iter_no=cur_state.iter_no + 1
	
	if cur_state!=None and cur_state.iter_no==engine.ITER_COUNT-1:
		raise Exception("All iterations over !")
	else:
		
		move_type=engine.COMMANDS[command]
		cur_pickup_pax=engine.get_pickups_pax(iter_no)
		base_map={}
		my_pos,cur_dir,pax_collected = engine.move_bus(my_pos,cur_dir,move_type,cur_pickup_pax,base_map)
		x,y=int(my_pos.split(",")[0]),int(my_pos.split(",")[1])	
		direction_x,direction_y=int(cur_dir.split(",")[0]),int(cur_dir.split(",")[1])
		new_state = models.BusState(bus_id=bus.id,iter_no=iter_no,x=x,y=y,direction_x=direction_x,direction_y=direction_y,pax_collected=pax_collected)
				
		db.session.add(new_state)
		db.session.commit()
		return my_pos,cur_dir,pax_collected