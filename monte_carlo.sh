 #!/bin/bash
workers=32
steps=10000000
 $(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task ${workers} --env base --script monte_carlo_pi.py -- --workers ${workers} --steps ${steps}) 