from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from openai_vision import analyze_and_prompt
from stable_diffusion import generate_image
import io

app = FastAPI(
    title="Digital Avatar Generator (GPT-4o + Stable Diffusion)",
    description="Upload selfie → choose style → get AI avatar in seconds",
    version="2.0"
)

@app.post("/avatar", response_class=StreamingResponse)
async def avatar(
    style: str = Form(..., description="Style of avatar", example="anime"),
    image: UploadFile = File(..., description="Your selfie (JPG/PNG)")
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    try:
        # Step 1: GPT-4o Vision → Smart Prompt
        prompt = analyze_and_prompt(style.lower(), image)
        print(f"[GPT-4o] Generated Prompt: {prompt}")

        # Step 2: Stable Diffusion → Avatar Image
        png_bytes = generate_image(prompt)

        return StreamingResponse(
            io.BytesIO(png_bytes),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=avatar_{style}.png"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Server Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "Go to /docs to test the avatar generator!"}