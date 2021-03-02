#!/bin/bash
echo "Running third test case - ./producer 20 10 189"
./producer 20 10 189 | grep Producing > producer_out.txt
./producer 20 10 189 | grep Consuming > consumer_out.txt
cat producer_out.txt | cut --complement --character 1-20 > producer_comp.txt
cat consumer_out.txt | cut --complement --character 1-20 > consumer_comp.txt
diff producer_comp.txt consumer_comp.txt > /dev/null
[ $? -eq 0 ] && echo "Third test case passed"