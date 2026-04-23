import asyncio
import time
import httpx
from processor import OLLAMA_URL

async def main():
    start = time.time()
    prompt = """
    Analiza este texto y devuelve un objeto JSON EXACTO con las claves: titulo, resumen.
    
    [Inicio de la transcripción]
    Laura: La prueba del motor Tronador II se retrasará debido al sistema de aviónica.
    [Fin]
    """
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False
    } # SIN FORMAT JSON
    try:
        async with httpx.AsyncClient(timeout=1200.0) as client:
            resp = await client.post(OLLAMA_URL, json=payload)
            print("Tiempo SIN format='json':", time.time() - start)
            
        start2 = time.time()
        payload["format"] = "json"
        async with httpx.AsyncClient(timeout=1200.0) as client:
            resp2 = await client.post(OLLAMA_URL, json=payload)
            print("Tiempo CON format='json':", time.time() - start2)
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
