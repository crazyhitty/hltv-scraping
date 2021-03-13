#!/bin/bash

nohup python3 run.py &

echo "Started scraping in background. Please stop the process by running stop.sh"
rm -rf run_py_pid
echo $! > run_py_pid