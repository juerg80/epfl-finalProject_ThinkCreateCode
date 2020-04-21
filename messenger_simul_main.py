import flask
from messenger_classes import *

# init
app = flask.Flask("Messenger Simul")
config_File="C:/Users/juerg/Documents/Admin/2020/Ausbildung/EPFL_Python/Code/Block_18/config_base.txt"
map_distances_file="C:/Users/juerg/Documents/Admin/2020/Ausbildung/EPFL_Python/Code/Block_18/map_distances.txt"
map_altitudes_file="C:/Users/juerg/Documents/Admin/2020/Ausbildung/EPFL_Python/Code/Block_18/map_altitudes.txt"

# define global variables
shift_id=0
config={}
map_distances=[]
map_altitudes=[]
my_map=map([],[],[])
current_shift={}
last_shift={}
riders=[]


# define some functions
def get_html(page_name):
    html_file=open(page_name + ".html")
    content=html_file.read()
    html_file.close()
    return content


# Specify routes
@app.route("/")
def homepage():
    return get_html("index")

@app.route("/init")
def init():
    global config
    global shift_id
    global current_shift
    global last_shift
    global my_map
    global riders

    config=init_config(config_File)
    shift_id=0
    map_distances=read_map(map_distances_file)
    map_altitudes=read_map(map_altitudes_file)
    my_map=map(config['map1'],map_distances,map_altitudes)
    riders=[]
    for i in range (0,int(config['NumberRiders'])):
        res=gen_rider(i+1,config)
        riders.append(res)

    current_shift=shift(dt.time(8,0,0),dt.time(12,0,0),shift_id,[],[],[])
    last_shift={}
    return get_html("index").replace("$$STATUS$$","Game initialised").replace("$$VARSTATS$$","Shift ID: " + str(shift_id))

@app.route("/PrepareNextShift")
def PrepareNextShift():
    global current_shift
    global last_shift

    last_shift=current_shift
    current_shift=prepare_next_shift(current_shift.shift_id,config,riders,last_shift)
    
    # Build html lists
    content_riders=current_shift.availRiders
    result_riders=""
    for line in content_riders:
         result_riders+="<p class='availRider'>"+ line.name +"</p>"

    content_orders=current_shift.orders
    result_orders=""
    count=1
    for line in content_orders:
        result_orders+="<p class='availOrders'>"+ str(count) +': ' + line.start_loc + ' - ' + line.start_time.strftime('%H:%M')  + ' - ' + line.end_loc + ' - '+ line.end_time.strftime('%H:%M') + ' - '+ str(line.volume) +"</p>"
        count=count+1

    # Build Forms
    num_riders=len(current_shift.availRiders)
    forms=""
    for i in range(0,num_riders):
        forms+=current_shift.availRiders[i].name + ": " + "<input type='text' name=" + current_shift.availRiders[i].name + " class='assign_rider_spec' value='Enter Orders in chronological order, separeted with ;'>"
    
    return get_html("assignment").replace("$$AVAILABLERIDERS$$",result_riders).replace("$$AVAILORDERS$$",result_orders).replace("$$ASSIGNMENT$$",forms)
    

@app.route("/GetRiderAssignment")
def GetRiderAssignment():
    global current_shift
    global last_shift

    num_riders=len(current_shift.availRiders)
    assignment_raw=[] 
    for i in range(0,num_riders):
        assignment=flask.request.args.get(current_shift.availRiders[i].name)
        assignment_raw.append(assignment) #=['2,1']
    
    # transform and check assignment
    assignment=transform_assignment(assignment_raw,current_shift)
    result_check_assignment=check_assignment(assignment)

    if result_check_assignment==False:
        #@work (erneuter assigment aufruf mit status fehlermeldung oder so...)
        pass

    # Build new shift
    current_shift=build_shift(current_shift,assignment,my_map)

    return get_html("index").replace("$$STATUS$$","Riders assigned").replace("$$VARSTATS$$",'Shift ID: '+ str(current_shift.shift_id))
    