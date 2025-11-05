import os
import torch
from diffusers import FluxPipeline
from utils import make_output_dir, load_prompts, save_metadata
from tqdm import tqdm

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


MODEL_NAME = "black-forest-labs/FLUX.1-dev"
PROMPT_FILE = os.path.join(REPO_ROOT, "prompts.txt")
OUTPUT_BASE = os.path.join(REPO_ROOT, "outputs")

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

print(f"Using device: {device}")

pipe = FluxPipeline.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    local_files_only=True,  # expects model to be prefetched/cached
).to(device)

output_dir = make_output_dir(OUTPUT_BASE)
prompts = load_prompts(PROMPT_FILE)

meta = {"model": MODEL_NAME, "prompts": prompts}
save_metadata(output_dir, meta)

for i, prompt in enumerate(tqdm(prompts, desc="Generating")):
    image = pipe(
        prompt,
        width=1024,
        height=1024,
        num_inference_steps=30,
        guidance_scale=7.5,
        negative_prompt="lowres, bad anatomy, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, watermark, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
        ).images[0]
    image.save(f"{output_dir}/img_{i:03d}.png")
