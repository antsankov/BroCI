#!/usr/bin/python


import arrow
from flask import *
from pymongo import *
from json import dumps

app = Flask(__name__)

client = MongoClient('localhost',27017)
db = client.brofiler
top_c = db.top
netstat_c = db.netstat
capstat_c = db.capstat 

@app.route('/')
def base_page(name=None): 
 
    #this is where we list our timestamp
    end  = arrow.get('2015-05-11T21:23:58.970460+00:00')
     
    
    #find anything in the top collection before the time stamp
    return render_template('base.html',test= top_graph('DUMMY_START',end,12),name=name)



class top_graph(object):

    def __init__(self, start_time, end_time, limit):
        result = []
        minimum = 1000000000
        maximum = 0

        for measure in top_c.find({'time' : {'$lte' : time.timestamp} }, { '_id': 0,'pid': 1,'cpu': 1,'time':1}).limit(limit):
            result.append(measure)

            if (result.time < minimum):
                minimum = result.time
            
            if (result.time > maximum):
                maximum = result.time
        
        self.result = result
        self.minimum = minimum 
        self.maximum = maximum 



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
