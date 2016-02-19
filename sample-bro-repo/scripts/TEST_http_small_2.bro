#bro files checks for "css" in the file and then logs it

@load profiler
@load base/frameworks/sumstats

event bro_init()
	{
	            profiler::init_test("sample_test_2",1.0);	
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	    if ("css" in original_URI)
		{
	            profiler::test_hit("sample_test_2");	
                }
	}

