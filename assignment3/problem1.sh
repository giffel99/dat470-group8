#!/bin/bash
workers=32
samples=10000000
iterations=1
$(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task ${workers} --env base --script problem1.py -- -i ${iterations} -s ${samples}  -w ${workers} -p resulting-plot -v -d)  

#$(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task 2 --env base --script problem1.py )