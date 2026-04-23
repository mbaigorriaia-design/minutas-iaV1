import httpx
import time
import json

async def test_ollama():
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2:latest",
                "prompt": "Hola, responde en 1 palabra.",
                "stream": False
            })
            print(f"Status: {resp.status_code}")
            print(f"Respuesta: {resp.json().get('response')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Tiempo total: {time.time() - start:.2f}s")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ollama())
