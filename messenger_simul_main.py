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
    config=init_config(config_File)
    shift_id=1
    map_distances=read_map(map_distances_file)
    map_altitudes=read_map(map_altitudes_file)
    map={"distances":map_distances,"altitudes":map_altitudes}
    current_shift={}
    last_shift={}
    return get_html("index").replace("$$STATUS$$","Game initialised")

@app.route("/PrepareNextShift")
def prepare_next_shift():
    last_shift=current_shift
    current_shift=prepare_next_shift()
    pass

@app.route("/GetRiderAssignment")
def get_rider_assignment():
    pass

@app.route("/BuildShift")
def build_shift():
    pass