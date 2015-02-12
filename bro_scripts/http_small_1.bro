#bro script checks for 'js' in a connection url and logs it

global x1:int = 0;


event bro_init()
	{

		print "small_script_1 starting!";
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	if ("js" in original_URI)
		{
			print "JS";
			x1+=1;
			print x1;
		}
	}


event bro_done()
	{
        
		print fmt("Small script is finished with: %s",x1);	
	}

