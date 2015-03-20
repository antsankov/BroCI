#!/usr/bin/python

import arrow
from flask import *
from pymongo import *
from json import dumps
from sets import Set
import git, os, shutil

#Initalize Flask
app = Flask(__name__)

#The connection to the DB 
client = MongoClient('localhost',27017)
db = client.brofiler
top_c = db.top
netstat_c = db.netstat
capstat_c = db.capstat

# See http://www.masnun.com/2012/01/22/fetching-remote-git-repo-with-python-in-a-few-lines-of-codes.html
def setup_repo(DIR_NAME,REMOTE_URL):

    #this is for a pull
    if os.path.isdir(DIR_NAME): 
        repo = git.Repo(DIR_NAME)
        origin = repo.remotes.origin
        origin.pull(origin.refs[0].remote_head)
    
    #this is if we need to remake the directory
    else:
        os.mkdir(DIR_NAME)
        repo = git.Repo.init(DIR_NAME)
        origin = repo.create_remote('origin',REMOTE_URL)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)
        
    local = DIR_NAME + '/local.bro'
    repo_scripts = DIR_NAME + '/scripts/ '

    #copy the local file from the pulled repo to the local on the system
    shutil.copy(local,'/usr/local/bro/share/bro/site')
    #move the scripts to the proper direcotry as well
    #use instead of shutil, because copytree sucks.  
    os.system("cp -rf "+ repo_scripts + '/usr/local/bro/share/bro/policy/scripts') 

def update_repo(REMOTE_URL):
    repo = git.Repo.init(REMOTE_URL)
    o = repo.remotes.origin
    o.pull()    
    

class capstat_graph(object):

    def __init__(self, start_time, end_time):

        self.start_time = start_time
        self.end_time = end_time 

        self.time_stamps = Set([]) 

        self.time_minimum = 2161728000  
        self.time_maximum = 0 

        for time_stamp in capstat_c.find({'time' : {"$lte" : end_time.timestamp,"$gte" : start_time.timestamp}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time']) 
            
            if time < self.time_minimum:
                self.time_minimum = time
            
            if time > self.time_maximum: 
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps) 

        speed_query = capstat_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp,"$gte" : start_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$mbps"}}}])
        
        self.speed_results = []          
        for speed in speed_query['result']: 
            self.speed_results.append(speed) 

        self.speed_maximum = 1.2 * float(capstat_c.find_one(sort=[("mbps",-1)])['mbps'])
        
class netstat_graph(object):

    def __init__(self, start_time, end_time):
        
        self.start_time = start_time
        self.end_time = end_time 
        
        self.time_stamps = Set([]) 

        self.time_minimum = 2161728000  
        self.time_maximum = 0 

        for time_stamp in netstat_c.find({'time' : {"$lte" : end_time.timestamp,"$gte" : start_time.timestamp}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time']) 
            
            if time < self.time_minimum:
                self.time_minimum = time
            
            if time > self.time_maximum: 
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps) 

        success_rate_query = netstat_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp,"$gte" : start_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$success"}}}])
        
        self.success_results = []          
        for success_rate in success_rate_query['result']: 
            self.success_results.append(success_rate)

class top_graph(object):

    def __init__(self, start_time, end_time):
        
        self.start_time = start_time
        self.end_time = end_time 
        
        self.time_stamps = Set([]) 

        self.time_minimum = 2161728000  
        self.time_maximum = 0

        for time_stamp in top_c.find({'time' : {"$lte" : end_time.timestamp,"$gte" : start_time.timestamp}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time']) 
            
            if time < self.time_minimum:
                self.time_minimum = time
            
            if time > self.time_maximum: 
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps) 
 
        cpu_query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp,"$gte" : start_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$cpu"}}}])
        
        self.cpu_results = []          
        for cpu_reading in cpu_query['result']: 
            self.cpu_results.append(cpu_reading) 

        #this gets a little bigger than the largest memory use, so we can add a y axis on our graph
        self.ram_maximum = 1.2 * top_c.find_one(sort=[("rss",-1)])['rss'] 

        ram_query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time.timestamp,"$gte" : start_time.timestamp}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$rss"}}}])
        
        self.ram_results = [] 
        for ram_reading in ram_query['result']: 
            self.ram_results.append(ram_reading) 

#######################################################################
#Initialize some test queries, in the future this should be in a method.

name = "Brofiler"
start = arrow.get('2014-05-11T21:23:58.970460+00:00')
end  = arrow.get('2015-05-11T21:23:58.970460+00:00')
top_sample = top_graph(start,end)
netstat_sample = netstat_graph(start,end)
capstat_sample = capstat_graph(start,end)


@app.route('/')
def base_page(name=None):
      return render_template('base.html',capstatSample=capstat_sample,topSample = top_sample,netstatSample = netstat_sample,name=name)

@app.route('/', methods=['POST'])
def init_git():
    remote = request.form['remote']
    setup_repo('GIT_REPO',remote)
    return render_template('base.html',capstatSample=capstat_sample,topSample = top_sample,netstatSample = netstat_sample,name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
