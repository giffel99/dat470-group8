 #!/bin/bash

 $(/opt/local/bin/run_job.sh --partition cpu-markov --cpus-per-task 12 --env base --script monte_carlo_pi.py -- --workers 1 --steps 1000)