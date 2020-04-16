import numpy
import datetime as dt


## Definition of classes and functions used in the game

def init_config(file):
    config={}
    fobj=open(file,"r")
    for line in fobj:
        line=line.strip()
        value=line.split(":")
        config[value[0]]=value[1]
    # convert map string to list
    config["map1"]=config["map1"].split(sep=',')
    fobj.close()
    return config

def read_map(file):
    map = numpy.loadtxt(file)
    return map

def getStatus():
    pass

# Modul: Prepare Next Shift
def prepare_next_shift(shift_id,config,last_shift={}):
    if shift_id==0: # initial state
        cash_last_shift=0
        rider_list=[]
        for i in range(0,int(config['NumberRiders'])):
            rider_list.append('f'+str(i+1))
        available_riders=rider_list
        time_shift={'t_start': dt.time(8,0,0),'t_end': dt.time(12,0,0)}
    else:
        cash_last_shift=get_cash_last_shift()
        available_riders=get_available_riders()
        time_shift=get_time_shift()
    
    order_list=get_orders()

    # init Shift
    new_shift=shift(time_shift['t_start'],time_shift['t_start'],shift_id+1,available_riders,order_list,{})
    return new_shift

def get_time_shift():
    pass

def get_cash_last_shift():
    #@work
    return 100

def get_orders():
    #@work
    order_list=[]
    order_1=order('A','10:00','B','12:00')
    order_2=order('C','09:00','D','11:30')
    order_list.append(order_1)
    order_list.append(order_2)
    return order_list

def get_available_riders():
    #@work
    rider_list=['f1']
    return rider_list

# Modul Build Shift

def transform_assignment(assignment_raw,current_shift):
    # transforms html params in dict
    num_riders=len(current_shift.availRiders)
    assignment={}
    for i in range (0,num_riders):
        assignment_list=assignment_raw[i].split(';')
        rider=current_shift.availRiders[i]
        assignment.update({rider:assignment_list})
    return assignment


def check_assignment(assignment):
    #@work
    return True

def build_shift(current_shift,assignment):
    tours={}
    num_riders=len(assignment)
    for i in range(0,num_riders):
        tour=get_tour(assignment[current_shift.availRiders[i]])
        tours.update({current_shift.availRiders[i]:tour})

    current_shift.tours=tours

    return current_shift


def get_tour(assignment_i):
    #@work
    


  

# Classes
class order:
    def __init__(self,start_loc,start_time,end_loc,end_time):
        self.start_loc=start_loc
        self.start_time=start_time
        self.end_loc=end_loc
        self.end_time=end_time
        self.volume=self.getVolume()

    def getVolume(self):
        #@work
        volume=200
        return volume


class rider:
    def __init__(self,name,nickname,avgSpeed,varSalary,fixSalary,reliability,workload):
        self.name=name
        self.nickname=nickname
        self.avgSpeed=avgSpeed
        self.varSalary=varSalary
        self.fixSalary=fixSalary
        self.varSalary=varSalary
        self.workload=workload # pensum

class shift:
    def __init__(self,t_start,t_end,shift_id,availRiders,orders,assignment):
        self.t_start=t_start
        self.t_end=t_end
        self.shift_id=shift_id # id
        self.availRiders=availRiders
        self.orders=orders
        self.weather=self.get_weather()
        self.agg_fine=self.get_agg_fine() # verkehrsbussen tot chf
        self.assignment=assignment
        self.tours={}
    
    def get_weather(self):
        #@work
        return 'sunny'
    
    def get_agg_fine(self):
        #@work
        return 75

class tour:
    pass

class step:
    pass

class company:
    pass

class cashaccount:
    pass