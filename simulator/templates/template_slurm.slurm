#!/bin/sh
#
#SBATCH --job-name=JOBNAME
#SBATCH -p hi_end
#SBATCH -w lisa
#SBATCH -c THREADS
#SBATCH -o slurmout/JOBNAME.%j.out
#SBATCH -e slurmout/JOBNAME.%j.err

mkdir -p slurmout/
ROOT/build/opt/zsim FILENAME
