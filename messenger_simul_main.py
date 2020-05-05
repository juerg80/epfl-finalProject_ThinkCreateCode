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
my_cash=cashaccount(0)


# define some functions
def get_html(page_name):
    html_file=open(page_name + ".html")
    content=html_file.read()
    html_file.close()
    return content


# Specify routes
@app.route("/")
def homepage():
    return get_html("index").replace("$$VARSTATS$$","Shift ID: " + str(shift_id)).replace("$$CASHACCOUNT$$",'Current Cash: ' + str(my_cash.tot))

@app.route("/init")
def init():
    global config
    global shift_id
    global current_shift
    global last_shift
    global my_map
    global riders
    global my_cash

    config=init_config(config_File)
    shift_id=0
    map_distances=read_map(map_distances_file)
    map_altitudes=read_map(map_altitudes_file)
    my_map=map(config['map1'],map_distances,map_altitudes)
    riders=[]
    for i in range (0,int(config['NumberRiders'])):
        res=gen_rider(i+1,config)
        riders.append(res)
    
    my_cash=cashaccount(int(config['Cash']))
    
    current_shift=shift(dt.time(8,0,0),dt.time(12,0,0),shift_id,[],[],config,[],my_map,my_cash.tot)
    last_shift={}
    return get_html("index").replace("$$STATUS$$","Game initialised").replace("$$VARSTATS$$","Shift ID: " + str(shift_id)).replace("$$CASHACCOUNT$$",'Current Cash: ' + str(my_cash.tot))

@app.route("/PrepareNextShift")
def PrepareNextShift():
    global current_shift
    global last_shift

    last_shift=current_shift
    current_shift=prepare_next_shift(current_shift.shift_id,config,riders,my_map,my_cash.tot,last_shift)
    
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
        forms+=current_shift.availRiders[i].name + ": " + "<input type='text' name=" + current_shift.availRiders[i].name + " class='assign_rider_spec' value='Enter Orders in chronological order, separeted with ;'>" + "<br><br>"
    
    return get_html("assignment").replace("$$AVAILABLERIDERS$$",result_riders).replace("$$AVAILORDERS$$",result_orders).replace("$$ASSIGNMENT$$",forms)
    

@app.route("/GetRiderAssignment")
def GetRiderAssignment():
    global current_shift
    global last_shift

    num_riders=len(current_shift.availRiders)
    assignment_raw=[] 
    for i in range(0,num_riders):
        assignment=flask.request.args.get(current_shift.availRiders[i].name)
        assignment_raw.append(assignment) # Format: ['2,1']
    
    # transform and check assignment
    assignment=transform_assignment(assignment_raw,current_shift)
    result_check_assignment=check_assignment(assignment)

    if result_check_assignment==False:
        #@work (erneuter assigment aufruf mit status fehlermeldung oder so...)
        pass

    # Build new shift
    current_shift.build_shift(assignment,my_map)

    # get Cash Booking and stats
    my_cash.add(current_shift.get_cash_booking())
    
    return get_html("index").replace("$$STATUS$$","Riders assigned").replace("$$VARSTATS$$",'Shift ID: '+ str(current_shift.shift_id)).replace("$$CASHACCOUNT$$",'Current Cash: ' + str(my_cash.tot))


@app.route("/ShowStats")
def show_stats():
    global current_shift

    current_shift.get_stats()

    # get html string
    result_stats=''
    for key in current_shift.stats:
        result_stats+="<p class='stats'>" + key + current_shift.stats[key] +"</p>"   
    return get_html('ShowStats').replace('$$SHIFTSTATS$$',result_stats)

@app.route("/ShowRiders")
def show_riders():
    # build html elements
    result_rider=''
    count=0
    for rider in riders:
        count=count+1
        result_rider+="<p class='rider'>" + "Rider Nr " + str(count)+"<br>" + \
            "*********<br>" + \
            "Name: "+rider.name +"<br>" + \
            "Nickname: "+rider.nickname +"<br>" + "Average Speed: "+rider.avgSpeed +"<br>" +  \
            "Variable Salary: "+rider.varSalary +"<br>" + "Fix Salary: "+rider.fixSalary +"<br>" + \
            "Workload: "+rider.workload +"<br>" + "Reliability: "+rider.reliability +"</p><br><br>"
    return get_html('ShowRiders').replace('$$SHOWRIDERS$$',result_rider)

@app.route("/ShowMap")
def show_map():
    # build html elements
    result_distance='<table>'
    result_altitude=''
    for i in range(0,len(my_map.locations)+1):
        for j in range(0,len(my_map.locations)+1):
            if i==0: # header
                if j==0:
                    result_distance += '<tr> <th> from \ to </th>'
                else:
                    result_distance += '<th>' + my_map.locations[j-1] +'</th>'
            else:
                if j==0:
                    result_distance += '<td>' + my_map.locations[i-1] + '</td>'
                else:
                    result_distance += '<td>' + str(my_map.distances[(i-1,j-1)])  +'</td>'
            
        result_distance += '</tr>'

    result_distance +='</table>'
    return get_html('ShowMap').replace('$$DISTANCES$$',result_distance)