#!/usr/bin/python

import arrow
from flask import *
from pymongo import *
from json import dumps

#profiler modules
from profiler_vc import setup_repo, update_repo
from unit_test import parse_unit, unit_test, run_tests 
from graphs import capstat_graph, netstat_graph, top_graph

#Initalize Flask
app = Flask(__name__)

#The connection to the DB 
client = MongoClient('localhost',27017)
db = client.brofiler
top_c = db.top
netstat_c = db.netstat
capstat_c = db.capstat

#############################
#Initialize some test queries 
############################

name = "Brofiler"
start = arrow.get('2014-05-11T21:23:58.970460+00:00').timestamp
end  = arrow.get('2016-05-11T21:23:58.970460+00:00').timestamp

top_sample = top_graph(start,end,top_c)
netstat_sample = netstat_graph(start,end,netstat_c)
capstat_sample = capstat_graph(start,end,capstat_c)

@app.route('/')
def base_page(name=None):

    return render_template('base.html',capstatSample=capstat_sample,topSample = top_sample,netstatSample = netstat_sample,name=name)


@app.route('/graphs', methods=['POST'])
def show_graphs(): 
    
    start_time = int(request.form['start_time']) / 1000
    end_time = int(request.form['end_time']) / 1000

    top_data = top_graph(start_time, end_time, top_c).__dict__
    netstat_data = netstat_graph(start_time,end_time,netstat_c).__dict__
    capstat_data = capstat_graph(start_time,end_time,capstat_c).__dict__ 

    response_dict = { 'top' : top_data, 'netstat' : netstat_data, 'capstat' : capstat_data } 
    response = json.dumps(response_dict)
    return response 

@app.route('/', methods=['POST'])
def index():

    if 'start-tests' in request.form:
        run_tests()

    elif 'remote' in request.form:
        remote = request.form['remote']
        setup_repo(remote)
    
    return render_template('base.html',capstatSample=capstat_sample,topSample = top_sample,netstatSample = netstat_sample,name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
