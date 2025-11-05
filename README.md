# FLUX image generation

This repository runs the `black-forest-labs/FLUX.1-dev` Diffusers pipeline for HPC. It includes:
- A prefetch step to download the model into a local cache (requires a Hugging Face token)
- A simple generation script that reads prompts from a text file and writes images to `outputs/`

## Quick start

1) Clone or open the repo directory in a terminal.

2) Create and activate a virtual environment.

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies.

```zsh
pip install -r requirements.txt
```

4) Create your `.env` from the template and add your Hugging Face token.

```zsh
cp .env.example .env
# then edit .env and set HF_TOKEN=hf_********************************
```

5) Prefetch the model weights into a local cache so the generation step can run offline.

```zsh
sbatch prefetch.sh
```
- This script will source `.env` and use `HF_TOKEN`.
- By default it writes to `./models` in this repo.

6) Generate images from `prompts.txt`.

```zsh
sbatch flux_job.sh
```
- Outputs go to `./outputs/<timestamp>/`.

## Files

- `run_flux.py` — Loads the cached model and generates images from prompts
- `utils.py` — Small helpers for output directory creation, metadata, and prompt loading
- `prefetch.sh` — Downloads the model into your local cache (reads `HF_TOKEN` from `.env`)
- `flux_job.sh` — Example SLURM job script to run generation on GPU nodes
- `prompts.txt` — One prompt per line; lines starting with `#` are ignored


## Configuration
The script uses `local_files_only=True`, so prefetch must succeed first.
Other configuration for logging, output and model are done in the `prefetch.sh`, `flux_job.sh` and `run_flux.py`.

## Security and git hygiene

- Secrets are stored in a local `.env` file which is ignored by git.
- Never commit your `HF_TOKEN`. The `.gitignore` here excludes `.env`, `logs/`, `outputs/`, and caches.