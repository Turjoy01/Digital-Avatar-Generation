# Digital Avatar Generator API  
**Turn any selfie into a stunning AI avatar in seconds**  
Powered by **OpenAI GPT-4o Vision** (smart prompt) + **Stable Diffusion 1.5** (image generation)

Live in 4–10 seconds even on CPU | No frontend needed – just use Swagger UI!

### Features
- Upload a selfie (JPG/PNG)
- Choose style: `cartoon | anime | realistic | superhero | fantasy | cyberpunk | oil-painting | pixel-art`
- GPT-4o Vision analyzes your face and writes a perfect prompt
- Stable Diffusion instantly generates a 512×512 avatar
- Returns PNG directly (download or display)

### Tech Stack
- FastAPI (backend)
- OpenAI GPT-4o (vision + chat)
- Stable Diffusion v1-5 (runwayml) – CPU friendly
- Python 3.9+

### Quick Start (Windows / Linux / Mac)

```bash
# 1. Clone the repo
git clone https://github.com/Turjoy01/Digital-Avatar-Generation.git
cd Digital-Avatar-Generator

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# or
.venv\Scripts\activate       # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt
# or one-liner:
pip install fastapi uvicorn[standard] python-multipart openai pillow python-dotenv diffusers torch accelerate transformers --no-cache-dir

# 4. Add your OpenAI API key
copy .env.example .env
# then edit .env and put your key:
OPENAI_API_KEY=sk-your-real-openai-key-here
```

### Run the server

```bash
uvicorn main:app --reload
```

Server will start at → http://127.0.0.1:8000  
Interactive docs (Swagger UI) → http://127.0.0.1:8000/docs

### How to use (in Swagger)
1. Open `/docs`
2. Click **POST /avatar**
3. Click "Try it out"
4. Choose a style (e.g. `anime`, `cartoon`, `cyberpunk`)
5. Upload your selfie
6. Execute → download your avatar instantly!

### Example styles you can type
```
cartoon       → Disney/Pixar style
anime         → Beautiful anime character
realistic     → 8K studio portrait
superhero     → Marvel/DC comic style
fantasy       → Elf warrior with magic
cyberpunk     → Neon futuristic look
oil-painting  → Classic Renaissance portrait
pixel-art     → 16-bit retro game character
```

### Performance
- First run: ~20–40 sec (model download + load)
- Next requests: 4–10 sec per avatar (CPU only)
- GPU = 1–2 sec (just change `DEVICE = "cuda"` in stable_diffusion.py)

### Folder Structure
```
Digital-Avatar-Generator/
├── main.py               → FastAPI app
├── openai_vision.py      → GPT-4o vision prompt generator
├── stable_diffusion.py   → SD pipeline
├── requirements.txt
├── .env                  → your OpenAI key (gitignored)
└── README.md
```

### License
MIT – feel free to use, modify, and share.

Made with Turjoy – Star the repo if you like it!
