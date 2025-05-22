#!/bin/bash
#SBATCH --job-name=af_plotter_batch
#SBATCH --mem=12GB
#SBATCH --time=01:00:00
#SBATCH --output=%x_%j.log
#SBATCH --partition=cpu-short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=your.email.com
#SBATCH --mail-type=END,FAIL


#change to your conda path
source /path/to/anaconda3/bin/activate afplotter

BATCH="path/to/batch_plotter.py"
AFPLOTTER="path/to/afplotter.py"
INPUTDIR="path/to/input/dir"

#change to your paths
python "$BATCH" "$INPUTDIR" "$AFPLOTTER" afplotter
