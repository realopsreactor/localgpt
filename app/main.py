from fastapi import FastAPI, Request, HTTPException
import os, requests

app = FastAPI()

# read config from env (set in docker-compose)
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://llm:8000/v1")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "dev-key")  # vLLM accepts any key
MODEL            = os.getenv("MODEL", "HuggingFaceTB/SmolLM2-1.7B-Instruct")

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM upstream error: {e}")

