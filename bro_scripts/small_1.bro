#bro script checks for '5001/tcp' in a packet and logs it

global x1:int = 0;

export {
        redef enum Log::ID += { small_1 };

        type hit_record: record {

                ts:           time     &log;
                hits:         int    &log;
        };
}


event bro_init()
	{
		Log::create_stream(small_1, [$columns=hit_record]);
		print "small_script_1 starting!";
	}

event new_packet(c:connection, p:pkt_hdr)
        {
        local now = network_time();
        if (5001/tcp == c$id$resp_p)
                {
                        x1+=1;
                        print "small HIT 1";
                        local rec0: hit_record = [$ts = now,
                                            $hits = x1];
                        Log::write(small_1,rec0);
                }
        } 

event bro_done()
	{
        
		print fmt("Small script is finished with: %s",x1);	
	}

