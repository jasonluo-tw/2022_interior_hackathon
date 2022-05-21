#!/bin/bash


for i in {0..10}
do
    TIME=`date +%Y%m%d%H%M`
    echo $i
    python crawl_address_googlemap.py >& ./log/crawl_"$TIME".log
   
    sleep 20m
done
