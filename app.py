from fastapi import FastAPI
import httpx

app = FastAPI()

MICROSERVICE_URL = "https://microservice-1-k15t.onrender.com"  # Replace with your Render service URL

@app.get("/compute")
async def compute(number: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MICROSERVICE_URL}/compute", params={"number": number})
        return response.json()