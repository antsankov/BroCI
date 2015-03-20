#bro files checks for "css" in the file and then logs it

global y:int = 0;

export {
        redef enum Log::ID += { small_2 };

        type hit_record: record {
                ts:           time     &log; 
                hits:         int    &log;
        };

}


event bro_init()
	{
		Log::create_stream(small_2, [$columns=hit_record]);
		print "small_script_2 starting!";
	}


event new_packet(c:connection, p:pkt_hdr)
        {
        local now = network_time();
        if (5002/tcp == c$id$resp_p)
                {
                        y+=1;
                        print "small HIT 2";
                        local rec0: hit_record = [$ts = now,
                                            $hits = y];
                        Log::write(small_2,rec0);
                }
        } 

event bro_done()
	{
        
		print fmt("Small script is finished with: %s",y);	
	}

