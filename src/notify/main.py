import base64
from typing import Union


from fastapi import FastAPI, Request

from routes import gmail_pub_sub_endpoint

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/notify")
async def handle_push(request: Request):
    body = await request.json()

    message = body.get("message")
    if message and "data" in message:
        data = base64.b64decode(message["data"]).decode("utf-8")
        print("Received message:", data)
    else:
        print("Invalid message format:", body)

    # Must return 200 to acknowledge the message
    return {"status": "OK"}

app.include_router(gmail_pub_sub_endpoint.router)