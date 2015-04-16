# This module is used for creating our different graphs on the page. 
# It makes the queries, and returns the data necessary for the javascript

from sets import Set

class capstat_graph(object):

    def __init__(self, start_time, end_time,capstat_c):
        
        self.start_time = start_time
        self.end_time = end_time

        print start_time
        print end_time


        self.time_stamps = Set([])

        self.time_minimum = 2161728000
        self.time_maximum = 0 

        for time_stamp in capstat_c.find({'time' : {"$lte" : end_time,"$gte" : start_time}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time'])

            if time < self.time_minimum:
                self.time_minimum = time

            if time > self.time_maximum:
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps)

        speed_query = capstat_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time,"$gte" : start_time}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$mbps"}}}])

        self.speed_results = []
        for speed in speed_query['result']: 
            self.speed_results.append(speed)
        print self.speed_results
        self.speed_maximum = 1.2 * float(capstat_c.find_one(sort=[("mbps",-1)])['mbps'])


class netstat_graph(object):

    def __init__(self, start_time, end_time,netstat_c):

        self.start_time = start_time
        self.end_time = end_time

        self.time_stamps = Set([])

        self.time_minimum = 2161728000
        self.time_maximum = 0

        for time_stamp in netstat_c.find({'time' : {"$lte" : end_time,"$gte" : start_time}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time'])

            if time < self.time_minimum:
                self.time_minimum = time

            if time > self.time_maximum:
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps)

        success_rate_query = netstat_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time,"$gte" : start_time}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$success"}}}])

        self.success_results = []
        for success_rate in success_rate_query['result']:
            self.success_results.append(success_rate)


class top_graph(object):

    def __init__(self, start_time, end_time, top_c):

        self.start_time = start_time
        self.end_time = end_time

        self.time_stamps = Set([])

        self.time_minimum = 2161728000
        self.time_maximum = 0

        for time_stamp in top_c.find({'time' : {"$lte" : end_time,"$gte" : start_time}}, {'time' : 1, '_id' : 0}):
            #just gets the the actual time int
            time = int(time_stamp['time'])

            if time < self.time_minimum:
                self.time_minimum = time

            if time > self.time_maximum:
                self.time_maximum = time

            self.time_stamps.add(time)

        #convert it to a list so it is json serializable
        self.time_stamps = list(self.time_stamps)

        cpu_query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time,"$gte" : start_time}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$cpu"}}}])

        self.cpu_results = []
        for cpu_reading in cpu_query['result']:
            self.cpu_results.append(cpu_reading)

        #this gets a little bigger than the largest memory use, so we can add a y axis on our graph
        self.ram_maximum = 1.2 * top_c.find_one(sort=[("rss",-1)])['rss']

        ram_query = top_c.aggregate([{ "$match" : {'time' : {'$lte' : end_time,"$gte" : start_time}}},{"$group":{"_id": "$identifier" ,'data': { "$push": "$rss"}}}])

        self.ram_results = []
        for ram_reading in ram_query['result']:
            self.ram_results.append(ram_reading)



