# FLUX image generation

This repository runs the `black-forest-labs/FLUX.1-dev` Diffusers pipeline on your machine or HPC. It includes:
- A prefetch step to download the model into a local cache (requires a Hugging Face token)
- A simple generation script that reads prompts from a text file and writes images to `outputs/`
- SLURM-friendly scripts that also work locally

## Quick start (macOS, zsh)

1) Clone or open the repo directory in a terminal.

2) Create and activate a virtual environment.

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies.

```zsh
pip install -U pip
pip install -r requirements.txt
```

4) Create your `.env` from the template and add your Hugging Face token.

```zsh
cp .env.example .env
# then edit .env and set HF_TOKEN=hf_********************************
```

5) Prefetch the model weights into a local cache so the generation step can run offline.

```zsh
bash prefetch.sh
```
- This script will source `.env` and use `HF_TOKEN`.
- By default it writes to `./.cache/models` in this repo. Customize via env vars:
  - `MODEL_NAME` (default `black-forest-labs/FLUX.1-dev`)
  - `JOBDIR` (defaults to `./.cache`)
  - `HF_HOME`, `DIFFUSERS_CACHE` if you want custom cache paths

6) Generate images from `prompts.txt`.

```zsh
python run_flux.py
```
- Outputs go to `./outputs/<timestamp>/`.
- You can override paths with env vars when calling:

```zsh
PROMPT_FILE=./prompts.txt OUTPUT_BASE=./outputs MODEL_NAME=black-forest-labs/FLUX.1-dev python run_flux.py
```

## Files

- `run_flux.py` — Loads the cached model and generates images from prompts
- `utils.py` — Small helpers for output directory creation, metadata, and prompt loading
- `prefetch.sh` — Downloads the model into your local cache (reads `HF_TOKEN` from `.env`)
- `flux_job.sh` — Example SLURM job script to run generation on GPU nodes
- `prompts.txt` — One prompt per line; lines starting with `#` are ignored

## SLURM usage (HPC)

- Prefetch on a CPU partition (adjust paths):
  - Ensure `.env` exists with `HF_TOKEN`.
  - Submit or run `prefetch.sh`. The `#SBATCH` lines are ignored when run as a normal shell script but recognized by `sbatch`.
- Run generation on a GPU partition:
  - Edit `flux_job.sh` to match your modules and paths.
  - `sbatch flux_job.sh`

Tip: both scripts honor these env vars if set: `MODEL_NAME`, `JOBDIR`, `HF_HOME`, `DIFFUSERS_CACHE`.

## Configuration

`run_flux.py` supports environment overrides and automatically loads `.env` from the repo root using `python-dotenv`:
- `MODEL_NAME` — HF model id (default `black-forest-labs/FLUX.1-dev`)
- `PROMPT_FILE` — Path to prompts file (default `./prompts.txt`)
- `OUTPUT_BASE` — Directory for generated images (default `./outputs`)

The script uses `local_files_only=True`, so prefetch must succeed first.

Tip: You can set the above variables either in your shell before running the script or inside `.env` — the Python script will read them automatically.

## Security and git hygiene

- Secrets are stored in a local `.env` file which is ignored by git.
- Never commit your `HF_TOKEN`. The `.gitignore` here excludes `.env`, `logs/`, `outputs/`, and caches.

## Troubleshooting

- Torch install issues (especially on Apple Silicon): follow the official PyTorch installation instructions for your platform.
- If `run_flux.py` errors with missing weights: re-run `bash prefetch.sh` and ensure `HF_TOKEN` is valid and the token has access to the model.
- If you want to change cache location, set `JOBDIR` or `HF_HOME` before running `prefetch.sh`.

## License

This repo contains scripts to run third-party models. Respect the licenses and terms for the model and datasets you use.
