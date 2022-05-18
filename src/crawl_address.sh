#!/bin/bash

TIME=`date +%Y%m%d%H%M`

for i in {0.10}
do
    /opt/homebrew/Caskroom/miniforge/base/bin/python3.8 /Users/luo-j/Documents/competition/2022_interior_hackathon/src/crawl_address_googlemap.py >& /Users/luo-j/Documents/competition/2022_interior_hackathon/src/log/crawl_"$TIME".log
    
    sleep 20m
done
