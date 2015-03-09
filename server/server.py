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
    test = top_graph(0,end,12)
    
    #find anything in the top collection before the time stamp
    return render_template('base.html',test= test,name=name)



class top_graph(object):

    def __init__(self, start_time, end_time, limit):
        
        self.start_time = start_time
        self.end_time = end_time
        
        
        minimum = 2161728000  
        maximum = 0

        results = []

        #for measure in top_c.find({'time' : {'$lte' : end_time.timestamp} }, { '_id': 0,'pid': 1,'cpu': 1,'time':1}).limit(limit):
        query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$cpu"}}}])
        
        for cpu_reading in query['result']: 
            results.append(cpu_reading)

        print results 
            
        self.results = results
        self.minimum = minimum 
        self.maximum = maximum 



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
