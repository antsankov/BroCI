module profiler;

export {
        redef enum Log::ID += { ci_results };
    
        type script_results: record 
            { 
                time_stamp:     time    &log;
                hits:           double  &log;
                script_name:    string  &log;
                pass_or_fail:   string  &log;
            };
        global test_vector: vector of string;
        global log_event: function(name: string,hits: double);   
        global init_test: function(test_name: string, threshold: double);
        global test_hit: function(stream_name: string);
        global pass_counter: int;
}

event bro_init()
    {
        print "CI Started";
        Log::create_stream(profiler::ci_results, [$columns=script_results]); 
    }

function init_test(test_name: string, threshold: double)
    {
        test_vector[0]= test_name;
        
        local r1 = SumStats::Reducer($stream= test_name, $apply=set(SumStats::SUM));
        SumStats::create([$name = test_vector[0],
                      $epoch = 1min,
                      $reducers = set(r1),
                      $threshold = threshold,
                      $threshold_val(key: SumStats::Key, result: SumStats::Result) =
                      {
                        print result[test_vector[0]]$sum;
                        return result[test_vector[0]]$sum;
                      },
                      $threshold_crossed(key: SumStats::Key, result: SumStats::Result) =
                      {
                        pass_counter = 0; 
                        print("THRESHOLD CROSSEED"); 
                        log_event(test_vector[0],result[test_vector[0]]$sum);
                      }]);
    }


#We need to call this method for every 
function log_event(name: string, hits: double) 
    {
        local p_or_f = "FAIL";
        if (pass_counter == 0)
        {
            p_or_f = "PASS";
        }
        
        local now = network_time();
        local script_name = name;  

        local rec0: script_results = [$time_stamp = now, 
                                      $hits = hits,  
                                      $script_name = script_name,
                                      $pass_or_fail = p_or_f
                                     ];   
        Log::write(ci_results,rec0);
    }

function test_hit(stream_name: string)
    {
     SumStats::observe(stream_name,
                SumStats::Key(),
                SumStats::Observation($num=1));
    }
