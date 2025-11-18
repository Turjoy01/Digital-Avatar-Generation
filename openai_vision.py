# openai_vision.py
import openai
from fastapi import UploadFile, HTTPException
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

STYLE_PROMPTS = {
    "cartoon": "Turn this person into a cute Disney/Pixar style cartoon character with big expressive eyes, vibrant colors, smooth shading, and clean outlines.",
    "anime": "Transform this person into a beautiful anime character with detailed sparkling eyes, flowing hair, vibrant colors, and manga-style shading.",
    "realistic": "Create an ultra-realistic professional portrait of this person, 8K quality, perfect skin, cinematic studio lighting, sharp details.",
    "superhero": "Reimagine this person as a powerful superhero in epic comic book style, dramatic pose, glowing effects, detailed costume.",
    "fantasy": "Turn this person into a majestic fantasy elf warrior with glowing eyes, intricate armor, ethereal lighting, and magical aura.",
    "cyberpunk": "Convert this person into a cyberpunk character with neon lights, holographic elements, futuristic outfit, rainy city night vibe.",
    "oil-painting": "Transform this person into a classical oil painting portrait in the style of Renaissance masters, rich textures, dramatic lighting.",
    "pixel-art": "Convert this person into detailed 16-bit pixel art character, retro game style, sharp pixels, vibrant palette."
}

def analyze_and_prompt(style: str, file: UploadFile) -> str:
    if style not in STYLE_PROMPTS:
        raise HTTPException(400, f"Invalid style. Choose from: {', '.join(STYLE_PROMPTS.keys())}")

    # Read and resize image
    contents = file.file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((512, 512))

    # Encode to base64
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    base64_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    base_prompt = STYLE_PROMPTS[style]
    full_prompt = f"{base_prompt}\n\nProvide a highly detailed, vivid, and professional prompt suitable for Stable Diffusion image generation. Focus on facial features, hair, expression, clothing, lighting, and overall art style. Make it 100-150 words long."

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"OpenAI API error: {str(e)}")