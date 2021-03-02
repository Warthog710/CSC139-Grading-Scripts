#!/bin/bash
echo "Running first test case - ./producer 10 20 124"
./producer 10 20 124 | grep Producing > producer_out.txt
./producer 10 20 124 | grep Consuming > consumer_out.txt
cat producer_out.txt | cut --complement --character 1-10 > producer_comp.txt
cat consumer_out.txt | cut --complement --character 1-10 > consumer_comp.txt
diff producer_comp.txt consumer_comp.txt > /dev/null
[ $? -eq 0 ] && echo "First test case passed"