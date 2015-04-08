from sets import Set

class capstat_graph(object):

    def __init__(self, start_time, end_time,capstat_c):
        
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

    def __init__(self, start_time, end_time,netstat_c):

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

