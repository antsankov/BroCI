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
    top  = arrow.get('2015-05-11T21:23:58.970460+00:00')
    
    result = []
    
    #find anything in the top collection before the time stamp
    for measure in top_c.find({'time' : {'$lte' : top.timestamp}}):
        result.append(measure) 
   
    return render_template('base.html',test=result,name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
