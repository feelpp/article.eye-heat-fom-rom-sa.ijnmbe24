#!/bin/bash
#SBATCH -J DSA                  # name of the job
#SBATCH -N 1                    # number of nodes
#SBATCH -n 12                   # number of cores
#SBATCH -t 06:45:00             # job duration
#SBATCH -o log/DSA%j_out.log    # standard output
#SBATCH -e log/DSA%j_err.log    # standard error

mpiexec -bind-to core python3 run-SA.py
