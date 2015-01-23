#bro script checks for 'js' in a connection url and logs it

global x:int = 0;

export {
        redef enum Log::ID += { small_1 };

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
		Log::create_stream(small_1, [$columns=hit_record]);
		print "small_script_1 starting!";
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	if ("js" in original_URI)
		{
			x+=1;
			local now = network_time(); 
			local info: hit_record = [$ts = now,
					    $hits = x];	
			Log::write(small_1,info);
		}
	}


event bro_done()
	{
        
		print fmt("Small script is finished with: %s",x);	
	}

