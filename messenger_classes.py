import numpy


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

def prepare_next_shift():
    pass

class order:
    pass

class rider:
    pass

class shift:
    pass

class tour:
    pass

class step:
    pass

class company:
    pass

class cashaccount:
    pass