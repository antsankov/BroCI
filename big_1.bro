global x0:int = 0;
global y0:int = 0;

export {
        redef enum Log::ID += { big_1 };

        type hit_record: record { 
                ts:           time     &log;
                hits:         int    &log;
        };
}


event bro_init()
	{
		Log::create_stream(big_1, [$columns=hit_record]);
		print "big_1 starting!";
	}

event new_packet(c:connection, p:pkt_hdr) 
	{
	local now = network_time(); 
	if (5001/tcp == c$id$resp_p)
		{
			x0+=1;
			print "BIG HIT 1";	
			local rec0: hit_record = [$ts = now,
					    $hits = x0];	
			Log::write(big_1,rec0);
		}
	

        if (5002/tcp == c$id$resp_p)
                {
                        y0+=1;
                        print "BIG HIT 2";
                        local rec1: hit_record = [$ts = now,
                                            $hits = y0];
                        Log::write(big_1,rec1);
                }
        }

event bro_done()
	{
        
		print fmt("big script 1 is finished with x: %s and y: %s",x0,y0);	
	}

