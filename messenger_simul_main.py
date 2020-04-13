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
map={}
current_shift={}
last_shift={}


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

    config=init_config(config_File)
    shift_id=0
    map_distances=read_map(map_distances_file)
    map_altitudes=read_map(map_altitudes_file)
    map={"distances":map_distances,"altitudes":map_altitudes}
    current_shift={}
    last_shift={}
    return get_html("index").replace("$$STATUS$$","Game initialised")

@app.route("/PrepareNextShift")
def PrepareNextShift():
    global current_shift
    global last_shift

    last_shift=current_shift
    current_shift=prepare_next_shift(shift_id,config,last_shift)
    
    # Build html lists
    content_riders=current_shift.availRiders
    result_riders=""
    for line in content_riders:
         result_riders+="<p class='availRider'>"+ line +"</p>"

    content_orders=current_shift.orders
    result_orders=""
    for line in content_orders:
         result_orders+="<p class='availOrders'>"+ line.start_loc + line.start_time + line.end_loc + line.end_time + str(line.volume) +"</p>"

    return get_html("assignment").replace("$$AVAILABLERIDERS$$",result_riders).replace("$$AVAILORDERS$$",result_orders)
    

@app.route("/GetRiderAssignment")
def GetRiderAssignment():
    pass

@app.route("/BuildShift")
def BuildShift():
    pass