# stable_diffusion.py
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io

DEVICE = "cpu"
TORCH_DTYPE = torch.float32

print(f"Loading Stable Diffusion 1.5 on {DEVICE} (this takes ~20-30 sec first time)...")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=TORCH_DTYPE,
    safety_checker=None,
    requires_safety_checker=False
)
pipe.to(DEVICE)
pipe.enable_attention_slicing()
print("Stable Diffusion loaded successfully!")

def generate_image(prompt: str) -> bytes:
    print(f"[SD] Generating image for: {prompt[:80]}...")
    image: Image.Image = pipe(
        prompt,
        num_inference_steps=15,      # 12-20 is fast & good quality
        guidance_scale=7.5,
        height=512,
        width=512
    ).images[0]

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()