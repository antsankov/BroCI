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
    start = arrow.get('2014-05-11T21:23:58.970460+00:00')
    end  = arrow.get('2015-05-11T21:23:58.970460+00:00')
    test = top_graph(start,end,12)
    
    #find anything in the top collection before the time stamp
    return render_template('base.html',test= test,name= name)



class top_graph(object):

    def __init__(self, start_time, end_time, limit):
        
        self.start_time = start_time
        self.end_time = end_time 
        
        self.time_stamps = [] 

        self.minimum = 2161728000  
        self.maximum = 0

        for time_stamp in top_c.find({'time' : {"$lte" : end_time.timestamp,"$gte" : start_time.timestamp}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = time_stamp['time'] 
            
            if time < self.minimum:
                self.minimum = time
            
            if time > self.maximum: 
                self.maximum = time

            self.time_stamps.append(time)
        
 
        query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp,"$gte" : start_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$cpu"}}}])
        
        self.results = []          
        for cpu_reading in query['result']: 
            self.results.append(cpu_reading) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
