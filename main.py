from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
import json
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="WhatsApp Receptionist")

# Read verify token from .env
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@app.get("/")
async def home():
    return {
        "message": "WhatsApp Receptionist Backend Running 🚀"
    }


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = "",
    hub_verify_token: str = "",
    hub_challenge: str = "",
):
    """
    Meta calls this endpoint once to verify the webhook.
    """

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)

    raise HTTPException(status_code=403, detail="Verification Failed")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Meta sends every incoming WhatsApp message here.
    """

    body = await request.json()

    print("\n========== Incoming Webhook ==========")
    print(json.dumps(body, indent=4))
    print("======================================\n")

    return {"status": "received"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)