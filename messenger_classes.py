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
def prepare_next_shift(shift_id,config,riders,map,cash_start,last_shift={}):
    if shift_id==0: # initial state
        available_riders=riders
        time_shift={'t_start': dt.time(8,0,0),'t_end': dt.time(12,0,0)}
    else:
        available_riders=get_available_riders(riders)
        time_shift=get_time_shift()
    
    order_list=get_orders()

    # init Shift
    new_shift=shift(time_shift['t_start'],time_shift['t_end'],shift_id+1,available_riders,order_list,config,{},map,cash_start)
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
            if i.isdigit()==False or int(i)==0:
                my_orderlist.append(None)
                break
            else:
                my_orderlist.append(order_list[int(i)-1])
        assignment.update({rider:my_orderlist})
    return assignment


def check_assignment(assignment):
    #@work
    return True

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
    
    def get_summary(self):
        # for stats output
        res='Start: '+ self.start_loc + '(' + str(self.start_time) + ') - End: '+ self.end_loc + '(' + str(self.end_time) + \
            ') - Volume: ' + str(self.volume)
        return res


class rider:
    def __init__(self,name,nickname,avgSpeed,varSalary,fixSalary,reliability,workload):
        self.name=name
        self.nickname=nickname
        self.avgSpeed=avgSpeed
        self.fixSalary=fixSalary
        self.varSalary=varSalary
        self.reliability=reliability
        self.workload=workload # pensum

class shift:
    def __init__(self,t_start,t_end,shift_id,availRiders,orders,config,assignment,map,cash_start):
        self.t_start=t_start
        self.t_end=t_end
        self.shift_id=shift_id # id
        self.availRiders=availRiders
        self.orders=orders
        self.config=config
        self.cash_start=cash_start
        self.weather=self.get_weather()
        self.agg_fine=self.get_agg_fine() # verkehrsbussen tot chf
        self.build_shift(assignment,map)
        self.cash_end=0
    
    def get_weather(self):
        #@work
        return 'sunny'
    
    def get_agg_fine(self):
        #@work
        return 75

    def check_missed_orders(self):
        # returns a list of orders which have not been assigned
        #@work
        return []

    def get_order_exec_summary(self):
        # returns dict with number of assigned and succ executed and assigned and failed
        num_success=0
        num_fail=0
        for tour in self.tours:
            for step in tour.steps:
                if step.flag=='Order' and step.is_fail==True:
                    num_fail=num_fail+1
                elif step.flag=='Order' and step.is_fail==False:
                    num_success=num_success+1
        res={'num_success':num_success,'num_fail':num_fail}
        return res
    
    def get_cash_booking(self):
        tot_amount=0

        # salaries
        if self.t_end==dt.time(22,0,0):
            #@work: book salaries
            pass
        
        # fines
        tot_amount=tot_amount-self.agg_fine

        # cash from tours (ass: sign correct)
        for tour in self.tours:
            for step in tour.steps:
                tot_amount=tot_amount+step.evaluate_step()
        
        # check for missed orders
        my_missed_orders=self.check_missed_orders()
        my_missed_volume_tot=0
        for order in my_missed_orders:
            my_missed_volume_tot=my_missed_volume_tot + order.volume 
        tot_amount=tot_amount + my_missed_volume_tot * float(self.config['PenaltyMissedOrder'])
        
        # overwrite cash_end
        self.cash_end=self.cash_start+tot_amount
        return tot_amount

    def get_stats(self):
        # build dict with stats to show to user
        res={}

        # shift id
        res.update({'Shift ID: ': str(self.shift_id)})
        
        # Orders
        num_orders=len(self.orders)
        res.update({'Total Number of incoming orders: ': str(num_orders)})

        num_missed=len(self.check_missed_orders())
        order_exec=self.get_order_exec_summary()
        num_successfully_exec_orders=order_exec['num_success']
        num_failed_execs=order_exec['num_fail']

        res.update({'Total Number of missed orders: ': str(num_missed)})
        res.update({'Total Number of assigned but failed orders: ': str(num_failed_execs)})
        res.update({'Total Number of successfully executed orders: ': str(num_successfully_exec_orders)})

        # assignment
        for key in self.assignment.keys():
            count=1
            for order in self.assignment[key]:
                if order == None:
                    res.update({'Assignment ' + key.name + ' : ' : 'No orders attributed'})
                else:
                    res.update({'Assignment ' + key.name + ' ' + str(count) + ': ' : order.get_summary() })
                    count=count+1

        # weather
        res.update({'Weather: ': self.weather})

        # fine
        res.update({'Tot Fines: ': str(self.agg_fine)})

        # cash
        res.update({'Cash at beginning of shift: ': str(self.cash_start)})
        res.update({'Cash at end of shift: ': str(self.cash_end)})

        self.stats=res

    def build_shift(self,assignment,map):
        tours=[]
        num_riders=len(assignment)
        for i in range(0,num_riders):
            my_rider=self.availRiders[i]
            my_tour=self.get_tour(my_rider,assignment[self.availRiders[i]],map)
            tours.append(tour(my_rider,my_tour))
        self.tours=tours
        self.assignment=assignment

    def get_tour(self,my_rider,my_orders,my_map):
        my_tour=[]
        if not(my_orders == [None]):
            num_orders=len(my_orders)
            num_steps=2+num_orders+(num_orders-1)
            count_order=-1
            for i in range(0,num_steps):
                if i==0:
                    flag='Transfer_init'
                    t_start=self.t_start
                    t_end_soll=my_orders[0].start_time
                    loc_start='Company'
                    loc_end=my_orders[0].start_loc
                    volume=0
                    rider=my_rider
                    map=my_map

                elif i==num_steps-1:
                    flag='Transfer_end'
                    t_start=my_orders[num_orders-1].end_time
                    t_end_soll=self.t_end
                    loc_start=my_orders[num_orders-1].end_loc
                    loc_end='Company'
                    volume=0
                    rider=my_rider
                    map=my_map

                elif i%2==0:
                    flag='Transfer'
                    t_start=my_orders[count_order].end_time
                    t_end_soll=my_orders[count_order+1].start_time
                    loc_start=my_orders[count_order].end_loc
                    loc_end=my_orders[count_order+1].start_loc
                    volume=0
                    rider=my_rider
                    map=my_map

                else:
                    count_order=count_order+1
                    flag='Order'
                    t_start=my_orders[count_order].start_time
                    t_end_soll=my_orders[count_order].end_time
                    loc_start=my_orders[count_order].start_loc
                    loc_end=my_orders[count_order].end_loc
                    volume=my_orders[count_order].volume
                    rider=my_rider
                    map=my_map
                    
                my_step=step(flag,t_start,t_end_soll,loc_start,loc_end,volume,rider,map,self.config)
                my_tour.append(my_step)
        return my_tour

class tour:
    def __init__(self,rider,steps):
        self.rider=rider
        self.steps=steps
        self.get_rework_steps()

    def get_rework_steps(self):
        # correkt start_times and set failure flag
        for i in range(0,len(self.steps)):
            if self.steps[i].flag=='Transfer':
                self.steps[i].t_start=self.steps[i-1].t_end_ist
                self.steps[i].t_end_ist=self.steps[i].get_t_end_ist()
                self.steps[i].is_fail=False
            elif self.steps[i].flag=='Transfer_init':
                self.steps[i].is_fail=False
            elif self.steps[i].flag=='Transfer_end':
                self.steps[i].t_start=self.steps[i-1].t_end_ist
                self.steps[i].t_end_ist=self.steps[i].get_t_end_ist()
                if self.steps[i].t_end_ist>self.steps[i].t_end_soll:
                    self.steps[i].is_fail=True
                else:
                    self.steps[i].is_fail=False
            elif self.steps[i].flag=='Order':
                self.steps[i].t_start=max(self.steps[i-1].t_end_ist,self.steps[i].t_start)
                self.steps[i].t_end_ist=self.steps[i].get_t_end_ist()
                if (self.steps[i-1].t_end_ist > self.steps[i].t_end_soll) or \
                    (self.steps[i].t_end_ist > self.steps[i].t_end_soll):
                    self.steps[i].is_fail=True
                else:
                    self.steps[i].is_fail=False



class step:
    def __init__(self,flag,t_start,t_end_soll,loc_start,loc_end,volume,rider,map,config):
        self.flag=flag
        self.t_start=t_start
        self.t_end_soll=t_end_soll
        self.loc_start=loc_start
        self.loc_end=loc_end
        self.volume=volume
        self.rider=rider
        self.map=map
        self.config=config
        self.avgSpeed_ist=self.get_avgSpeed_ist(rider)
        self.t_end_ist=self.get_t_end_ist()
        self.bike_issue=self.get_bikeIssue()
        self.is_fail=''
        

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
        Tot_mins=self.t_start.minute + int((my_distance/self.avgSpeed_ist)*60)
        mins=Tot_mins % 60
        hours=int((Tot_mins - mins) / 60)        
        t_end_ist=dt.time(self.t_start.hour + hours , mins)
        return t_end_ist
    
    def evaluate_step(self):
        # gets brutto cash revenue from step
        if self.flag=="Order":
            if self.is_fail==True:
                res=-self.volume * float(self.config['PenaltyMissedOrder'])
            else:
                res=self.volume
        else:
            res=0

        return res




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
    def __init__(self,initial_cash):
        self.tot=initial_cash
    
    def add(self,amount):
        if amount<0:
            res=self.remove(-amount)
        else:
            self.tot=self.tot+amount
            res=1
        return res


    def remove(self,amount):
        if amount>self.tot:
            res=0
        else:
            self.tot=self.tot-amount
            res=1
        return res
