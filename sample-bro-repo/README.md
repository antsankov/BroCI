# Example BroCI repository 

## Local.bro
We make sure that all of our scripts are properly referenced and loaded in the local.bro file.

## unittest.yaml
This is the file where we can specify the tests we want to run. 
 * ```source``` - this is the source of the test, right now we only support ```PCAP```. 
 * ```pcap``` - the destination of the pcap file. 
 * ```count``` - how many times we want to run the traffic file through our generator. 
 * ```interface``` - the interface we want our traffic generator to output on. 

## scripts/
* This is where we store our scripts to be tested and referenced by the local.bro. 
* Some notes on adding scripts to this dirctory: 
  - They need to have ```@load profiler``` at the top of them so we can access our profiling functions 
  - In the bro_init event, you need to instantiate the test. Do this with a line like ```profiler::init_test("sample_test_1",1.0);```
  - In the event you want to test, register a hit with the command: ```profiler::test_hit("sample_test_1");```

## pcap/
* Store our pcap files in this directory. 
