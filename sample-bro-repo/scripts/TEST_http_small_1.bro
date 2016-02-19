#bro script checks for 'js' in a connection url and logs it
@load profiler 
@load base/frameworks/sumstats


event bro_init()
	{ 
            profiler::init_test("sample_test_1",1.0);
	}
 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
            local test_pattern = /js+/;
	    if (test_pattern in original_URI)
		{
                      profiler::test_hit("sample_test_1");		       
	        }
        }


