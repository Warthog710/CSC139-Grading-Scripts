#!/bin/bash
echo "Running second test case - ./producer 20 20 167"
./producer 20 20 167 | grep Producing > producer_out.txt
./producer 20 20 167 | grep Consuming > consumer_out.txt
cat producer_out.txt | cut --complement --character 1-20 > producer_comp.txt
cat consumer_out.txt | cut --complement --character 1-20 > consumer_comp.txt
diff producer_comp.txt consumer_comp.txt > /dev/null
[ $? -eq 0 ] && echo "Second test case passed"