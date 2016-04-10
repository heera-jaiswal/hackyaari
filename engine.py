import json
import os	
TEMP_DIR="D:/repo/hackyaari/env/data/temp"

TURN_LEFT=2
TURN_RIGHT=1
MOVE_FORWARD=0
RESET=3
COMMANDS={"MOVE_FORWARD":MOVE_FORWARD,"TURN_LEFT":TURN_LEFT,"TURN_RIGHT":TURN_RIGHT,"RESET":RESET}
#DIRECTION
POSITIVE_X=(1,0)
POSITIVE_Y=(0,1)
NEGATIVE_X=(-1,0)
NEGATIVE_Y=(0,-1)

all_iter_pickups_pax=None
TOTAL_PAX=3000
ITER_COUNT=1000
PAX_LIFE=40


def create_base_map():
	#0b100000000010000000001000000000
	one_lane=int(0b1000000000,2)
	grids_3=int(0b100000000010000000001000000000,2)
	row=[grids_3 & 0 ,grids_3,grids_3]	
	base_map=[row]*9*10
	return  base_map

def create_pax_feeds(pickups,total_pax,iter_count):		
	import random
	import copy
	pax=[]	
	iter_pickups=[]
	for i in range(iter_count):

		iter_pickups.append(copy.deepcopy(pickups))

	for i in range(total_pax):
		x=random.randint(1,8)
		y=random.randint(1,8)
		bin_x=10*x
		bin_y=10*y
		iter_index=random.randint(0,iter_count-1)		
		#pax.append((bin_x,bin_y,iter_index))
		key=str(bin_x)+","+str(bin_y)
		#if key in pickups.keys():				
		iter_pickups[iter_index][key].append(i)			
	
	return iter_pickups

def create_pickups_map():
	#0b100000000010000000001000000000
	pickups={}
	#one_lane=int('0b1000000000',2)	
	#grids_3=int('0b100000000010000000001000000000',2)
	#pickup_row=[grids_3 & 0 ,grids_3,grids_3]	
	#non_pickup_row=[0 , 0, 0]	
	pickups_map=[]
	for y in range(9*10):
		if y!=0 and y%10==0:			
			#pickups_map.append(pickup_row)
			x=10
			while x<90:
				pickups[str(x)+","+str(y)]=[]
				x+=10
		#else:
		#	pickups_map.append(non_pickup_row)			
	return pickups

def update_map(cur_map,iter_no,cur_pickups,pax_life):
	#grids_3=int('0b111111111111111111111111111111',2)	
	#int_bus_x=bus_position[0]/30
	#bin_bus_x=(grids_3) & (1<<(bus_position[0]%30))
	#bus_y=bus_position[1]
	#cur_map[int_bus_x][]
	#cur_pickups=iter_pickups[iter_no]
	if iter_no==0:		
		for key in cur_pickups.keys():
			cur_map[key]=[]	
	for key in cur_map.keys():
		cur_map[key] = [pax -1 for pax in cur_map[key]]


	#for key in cur_map.keys():		
	#	cur_map[key]= filter(lambda x: x != -1, cur_map[key])		

			
		#[pax -1 for pax in ]:

	
	#print cur_pickups[cur_pickups.keys()[0]]
	for key in cur_pickups.keys():
		cur_map[key].extend([pax_life]*len(cur_pickups[key]))

def check_move(x,y,base_map):
	pass
	return True
def move_bus(my_pos,cur_dir,move_type,cur_map,base_map):
	x,y=int(my_pos.split(",")[0]),int(my_pos.split(",")[1])	
	direction=tuple((int(cur_dir.split(",")[0]),int(cur_dir.split(",")[1])))
	if move_type==MOVE_FORWARD:
		if check_move(x,y,base_map)==True:
			x,y=x+direction[0],y+direction[1]
		else:
			pass
	elif move_type==TURN_LEFT:
		sign=(1 | direction[0],1 | direction[1])
		direction=(sign[1]*-1*(abs(direction[0])^ 1),sign[0]*(abs(direction[1])^ 1))
	elif move_type==TURN_RIGHT:
		sign=(1 | direction[0],1 | direction[1])
		direction=(sign[1]*(abs(direction[0])^ 1),sign[0]*-1*(abs(direction[1])^ 1))	
	

	my_pos,cur_dir = ",".join([str(x),str(y)]),",".join([str(direction[0]),str(direction[1])])
	pax_collected=0
	if 	my_pos in cur_map:
		pax_collected=len(filter(lambda x: x > -1, cur_map[my_pos]))
		#cur_map[my_pos]=[]

	return my_pos,cur_dir,pax_collected

def init_map_feed(reset=False):	
	base_map_path=os.path.join(TEMP_DIR,'base_map.txt')
	if reset==True:
		pickups = create_pickups_map()
		iter_pickups = create_pax_feeds(pickups,TOTAL_PAX,ITER_COUNT)
		#print iter_pickups		
		with open(base_map_path,"wb") as f:
			f.write(json.dumps({"map":iter_pickups}))
		cur_map={}
		for i in range(ITER_COUNT):
			cur_pickups=iter_pickups[i]
			update_map(cur_map,i,cur_pickups,PAX_LIFE)
			path=os.path.join(TEMP_DIR,str(i)+'_map.txt')
			with open(path,"wb") as f:
				f.write(json.dumps({"map":cur_map}))
	else:
		pass
	str_data=None
	with open(base_map_path,"rb") as f:
		str_data=f.read()
	json_data=json.loads(str_data)
	all_iter_pickups_pax=json_data["map"]

def get_pickups_pax(iter_no):	
	left_time=40	
	if all_iter_pickups_pax==None:
		init_map_feed()	
	path=os.path.join(TEMP_DIR,str(iter_no)+'_map.txt')
	str_map=None
	with open(path,"rb") as f:
		str_data=f.read()	
	json_data=json.loads(str_data)
	pickups_pax = json_data["map"]
	# pickups_pax_alive={}
	# for pickup in pickups_pax:
	# 	pax=pickups_pax[pickup]
	# 	alive_pax=filter(lambda x: x > -1, pax)
	# 	pickups_pax_alive[pickup]=alive_pax
	return pickups_pax

# def save_pax_feed(iter_pickups,pax_feed_no=0):	
# 	models.PaxFeed.query.filter_by(pax_feed_no=pax_feed_no).delete()
# 	db.session.commit()
# 	iter_no=0
# 	print "cleared iter_pickups (%d)" % pax_feed_no
# 	for pickups in iter_pickups:
# 		for pickup in pickups.keys():
# 			pax=",".join([str(p) for p in pickups[pickup]])
# 			x,y=(int(pickup.split(",")[0]),int(pickup.split(",")[1]))
# 			pax_feed = models.PaxFeed(pax_feed_no=pax_feed_no,x=x,y=y,pax=pax,iter_no=iter_no)			
# 			db.session.add(pax_feed)
# 		print iter_no
# 		iter_no+=1
# 		db.session.commit()

if __name__=="__main__":	
	# iter_count=1000
	# left_time=40
	# total_pax=3000
	# #map_,
	# pickups = create_pickups_map()
	# iter_pickups = create_pax_feeds(pickups,total_pax,iter_count)
	# #print iter_pickups
	# with open('base_map.txt',"wb") as f:
	# 	f.write(json.dumps({"map":iter_pickups}))

	# save_pax_feed(iter_pickups)
	# exit()	
	# cur_map={}
	# total_pax_collected=0
	# my_pos="0,0"
	# cur_dir="1,0"
	# for i in range(30):
	# 	my_pos,cur_dir,pax_collected = move_bus(my_pos,cur_dir,MOVE_FORWARD,cur_map,{})
	# my_pos,cur_dir,pax_collected = move_bus(my_pos,cur_dir,TURN_LEFT,cur_map,{})
	# print my_pos,cur_dir,pax_collected
	# print "------------------------------------------------------------------------------------------------------------------------------------------"
	# for i in range(iter_count):
	# 	cur_pickups=iter_pickups[i]
	# 	update_map(cur_map,i,cur_pickups,left_time)
	# 	path=os.path.join(TEMP_DIR,str(i)+'_map.txt')
	# 	with open(path,"wb") as f:
	# 		f.write(json.dumps({"map":cur_map}))

	# 	my_pos,cur_dir,pax_collected = move_bus(my_pos,cur_dir,MOVE_FORWARD,cur_map,{})
	# 	total_pax_collected+=pax_collected
	# 	if pax_collected>0:
	# 		print i,my_pos,cur_dir,total_pax_collected
		
		
	# print total_pax_collected
	init_map_feed()
	d=get_pickups_pax(101)
	with open("temp.txt","wb") as f:
		f.write(json.dumps(d))


	
	