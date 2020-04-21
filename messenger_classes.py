import numpy
import datetime as dt


## Definition of classes and functions used in the game

# Modul Init
def init_config(file):
    config={}
    fobj=open(file,"r")
    for line in fobj:
        line=line.strip()
        value=line.split(":")
        config[value[0]]=value[1]

    # convert some strings to lists
    config["map1"]=config["map1"].split(sep=',')
    config["RiderNames"]=config["RiderNames"].split(sep=',')

    fobj.close()
    return config

def gen_rider(id,config):
    name=config['f'+str(id) + '_name']
    nickname=config['f'+str(id)+'_nickname']
    avgSpeed=config['f'+str(id)+'_avgSpeed']
    varSalary=config['f'+str(id)+'_varSalary']
    fixSalary=config['f'+str(id)+'_fixSalary']
    workload=config['f'+str(id)+'_workload']
    reliability=config['f'+str(id)+'_reliability']

    res=rider(name,nickname,avgSpeed,varSalary,fixSalary,reliability,workload)
    return res

def read_map(file):
    map = numpy.loadtxt(file)
    return map

def getStatus():
    pass

# Modul: Prepare Next Shift
def prepare_next_shift(shift_id,config,riders,last_shift={}):
    if shift_id==0: # initial state
        cash_last_shift=0
        available_riders=riders
        time_shift={'t_start': dt.time(8,0,0),'t_end': dt.time(12,0,0)}
    else:
        cash_last_shift=get_cash_last_shift()
        available_riders=get_available_riders(riders)
        time_shift=get_time_shift()
    
    order_list=get_orders()

    # init Shift
    new_shift=shift(time_shift['t_start'],time_shift['t_start'],shift_id+1,available_riders,order_list,{})
    return new_shift

def get_time_shift():
    #@work
    return {'t_start': dt.time(8,0,0),'t_end': dt.time(12,0,0)}

def get_cash_last_shift():
    #@work
    return 100

def get_orders():
    #@work
    order_list=[]
    order_1=order('A',dt.time(10,0,0),'B',dt.time(12,0,0))
    order_2=order('C',dt.time(9,0,0),'D',dt.time(11,30,0))
    order_list.append(order_1)
    order_list.append(order_2)
    return order_list

def get_available_riders(riders):
    #@work
    rider_list=riders
    return rider_list

# Modul Build Shift

def transform_assignment(assignment_raw,current_shift):
    # transforms html params in dict
    num_riders=len(current_shift.availRiders)
    assignment={}
    order_list=current_shift.orders
    for i in range (0,num_riders):
        assignment_list=assignment_raw[i].split(';')
        rider=current_shift.availRiders[i]
        my_orderlist=[]
        for i in assignment_list:
            my_orderlist.append(order_list[int(i)-1])

        assignment.update({rider:my_orderlist})
    return assignment


def check_assignment(assignment):
    #@work
    return True

def build_shift(current_shift,assignment,map):
    tours={}
    num_riders=len(assignment)
    for i in range(0,num_riders):
        tour=get_tour(current_shift.availRiders[i],assignment[current_shift.availRiders[i]],map)
        tours.update({current_shift.availRiders[i]:tour})

    current_shift.tours=tours

    return current_shift


def get_tour(my_rider,my_orders,map):
    num_orders=len(my_orders)
    num_steps=2+num_orders+(num_orders-1)
    my_tour=[]
    count_order=-1
    for i in range(0,num_steps):
        if i==0:
            flag='Transfer_init'
        elif i==num_steps-1:
            flag='Transfer_end'
        elif i%2==0:
            flag='Transfer'
        else:
            flag='Order'
            count_order=count_order+1

        my_step=step(flag,my_orders[count_order].start_time,my_orders[count_order].end_time,
                    my_orders[count_order].start_loc,my_orders[count_order].end_loc,my_orders[count_order].volume,
                    my_rider,map)
        my_tour.append(my_step)
    return my_tour


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
        self.reliability=reliability
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
    def __init__(self,rider,steps):
        self.rider=rider
        self.steps=steps

class step:
    def __init__(self,flag,t_start,t_end_soll,loc_start,loc_end,volume,rider,map):
        self.flag=flag
        self.t_start=t_start
        self.t_end_soll=t_end_soll
        self.loc_start=loc_start
        self.loc_end=loc_end
        self.volume=volume
        self.rider=rider
        self.map=map
        self.avgSpeed_ist=self.get_avgSpeed_ist(rider)
        self.t_end_ist=self.get_t_end_ist()
        self.bike_issue=self.get_bikeIssue()
        

    def get_bikeIssue(self):
        #@work
        # 0: no issue
        # 1: minor_issue
        # 2: big_issue
        # 3: major_issue
        return 0

    def get_avgSpeed_ist(self,rider):
        #@work
        avgSpeed=int(rider.avgSpeed)
        return avgSpeed

    def get_t_end_ist(self):
        my_distance=self.map.get_distance(self.loc_start,self.loc_end)
        t_end_ist=dt.time(self.t_start.hour, self.t_start.minute + int((my_distance/self.avgSpeed_ist)*60))
        return t_end_ist


class map:
    def __init__(self,locations,distances,altitudes):
        self.locations=locations
        self.altitudes=altitudes
        self.distances=distances
    
    def get_distance(self,loc_start,loc_end):
        #@work
        return 20

    def get_altitudes(self,loc_start,loc_end):
        #@work
        return 50

class company:
    pass

class cashaccount:
    pass