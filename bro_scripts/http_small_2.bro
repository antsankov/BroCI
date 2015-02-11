#bro files checks for "css" in the file and then logs it

global y:int = 0;

export {
        redef enum Log::ID += { small_2 };

        type hit_record: record {
                ## Timestamp for when the measurement occurred.
                ts:           time     &log;
                
                ## Number of missed ACKs from the previous measurement interval.
                hits:         int    &log;
        };

}


event bro_init()
	{
		Log::create_stream(small_2, [$columns=hit_record]);
		print "small_script_2 starting!";
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	if ("css" in original_URI)
		{
			y+=1;
			local now = network_time(); 
			local info: hit_record = [$ts = now,
					    $hits = y];	
			Log::write(small_2,info);
		}
	}


event bro_done()
	{
        
		print fmt("Small script is finished with: %s",y);	
	}

