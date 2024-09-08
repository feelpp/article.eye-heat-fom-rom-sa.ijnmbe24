#!/bin/bash
#SBATCH -J heat-eye                     # name of the job
#SBATCH -N 1                            # number of nodes
#SBATCH --ntasks-per-node=12            # number of MPI processes per node
#SBATCH -t 02:20:00                     # job duration
#SBATCH --threads-per-core=1            # no hyperthreading
#SBATCH -o log/heat-eye-%j_out.log      # standard output
#SBATCH -e log/heat-eye-%j_err.log      # standard error

mpiexec -bind-to core feelpp_toolbox_heat --config-file eye.cfg