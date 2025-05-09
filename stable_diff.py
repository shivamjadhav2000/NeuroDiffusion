# stable_diff.py
import torch
from diffusers import StableDiffusionPipeline

# Load only once
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

def generate_image(prompt, filename="output.png"):
    image = pipe(prompt).images[0]
    image.save(filename)
    return filename
