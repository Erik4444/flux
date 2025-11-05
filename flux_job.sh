#!/bin/bash
#SBATCH --job-name=flux_runner
#SBATCH --partition=gpua100
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --time=00:05:00
#SBATCH --output=./logs/flux_%j.log


# Hugging Face Cache hierhin umleiten
export HF_HOME=./models
export DIFFUSERS_CACHE=$HF_HOME

module purge
module load palma/2022a
module load GCCcore/11.3.0
module load Python/3.10.4
module load palma/2023a
module load CUDA/12.1.1
source ./venv/bin/activate

python ./run_flux.py

echo "Job finished at $(date)"
