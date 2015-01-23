global x0:int = 0;
global y0:int = 0;

export {
        redef enum Log::ID += { big_1 };

        type hit_record: record {
                ## Timestamp for when the measurement occurred.
                ts:           time     &log;
                
                ## Number of missed ACKs from the previous measurement interval.
                hits:         int    &log;
        };

        ## The interval at which capture loss reports are created.
        const watch_interval = 1secs &redef;
}


event bro_init()
	{
		Log::create_stream(big_1, [$columns=hit_record]);
		print "big_1 starting!";
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	local now = network_time(); 
	if ("js" in original_URI)
		{
			x0+=1;
			
			local rec0: hit_record = [$ts = now,
					    $hits = x0];	
			Log::write(big_1,rec0);
		}
	
	if ("css" in original_URI)
                {
                        y0+=1;                        
                        local rec1: hit_record = [$ts = now,
                                            $hits = y0];
                        Log::write(big_1,rec1);
                }

	}


event bro_done()
	{
        
		print fmt("big script 1 is finished with x: %s and y: %s",x0,y0);	
	}

