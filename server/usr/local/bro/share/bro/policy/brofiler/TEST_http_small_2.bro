#bro files checks for "css" in the file and then logs it

global y:int = 0;



event bro_init()
	{
		print "small_script_2 starting!";
	}


 
event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string)
	{
	if ("css" in original_URI)
		{
			print "CSS";
			y+=1;
			print y;
		}
	}


event bro_done()
	{
        
		print fmt("Small script is finished with: %s",y);	
	}

