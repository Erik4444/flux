#!/bin/bash
#SBATCH --job-name=hf-prefetch
#SBATCH --partition=normal          # Optional: ignored when run locally
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --time=00:10:00
#SBATCH --output=./logs/prefetch_%j.log

set -euo pipefail

# Load secrets from .env if present (HF_TOKEN, optional overrides)
if [ -f ./.env ]; then
	set -a
	# shellcheck disable=SC1091
	source ./.env
	set +a
fi

# Where to store cached models; defaults to a local .cache directory if not provided
export HF_HOME="./models"
export DIFFUSERS_CACHE=$HF_HOME

# Required: HF_TOKEN must be set via environment or .env
if [ -z "${HF_TOKEN:-}" ]; then
	echo "Error: HF_TOKEN is not set. Create a .env file with HF_TOKEN=... or export it in your shell."
	exit 1
fi

# Allow overriding model name via env; default to FLUX.1-dev
MODEL_NAME="black-forest-labs/FLUX.1-dev"

# Minimal Python snippet to prefetch weights/tokenizer into cache
python - <<'PY'
import os
from diffusers import FluxPipeline
model = os.environ.get("MODEL_NAME", "black-forest-labs/FLUX.1-dev")
token = os.environ.get("HF_TOKEN")
FluxPipeline.from_pretrained(model, token=token, low_cpu_mem_usage=True)
print("Prefetch done into:", os.environ.get("HF_HOME"))
PY

echo "Cached models under: $HF_HOME"
du -sh "$HF_HOME"/hub/models--black-forest-labs--FLUX.1-* || true