 #!/bin/bash
workers=8
steps=10000000
seed=3
# $(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task ${workers} --env base --script monte_carlo_pi.py -- --workers ${workers} --steps ${steps} --seed ${seed} )  
$(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task ${workers} --env base --script problem-2-3.py -- --workers ${workers} --steps ${steps} --seed ${seed} )  