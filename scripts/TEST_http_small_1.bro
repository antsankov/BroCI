#bro script checks for 'js' in a connection url and logs it
@load profiler 
@load base/frameworks/sumstats


event bro_init()
	{
            #Setup the test and the threshold we want to pass  
            profiler::init_test("sample_test_1",1.0);
	}
 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	    if ("js" in original_URI)
		{
                    ##########################
                    #REGULAR SCRIPT GOES HERE#
                    #########################

                    #We can add a hit to the test, and it will check if the threshold is crossed
                    profiler::test_hit("sample_test_1");		       
	        }
        }


