#!/bin/bash
echo "Running fourth test case - ./producer 10 1000 145"
./producer 10 1000 145 | grep Producing > producer_out.txt
./producer 10 1000 145 | grep Consuming > consumer_out.txt
cat producer_out.txt | cut --complement --character 1-10000 > producer_comp.txt
cat consumer_out.txt | cut --complement --character 1-10000 > consumer_comp.txt
diff producer_comp.txt consumer_comp.txt > /dev/null
[ $? -eq 0 ] && echo "Fourth test case passed"