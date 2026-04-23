from fastapi import FastAPI, HTTPException, File, UploadFile
import os
import datetime
import docx
import io
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from processor import extract_structured_minutes

app = FastAPI(title="Minutas-IA V1 API")

# Configuración de CORS para tu frontend en Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    transcript: str

@app.get("/")
async def root():
    return {"message": "Minutas-IA V1 API is running"}

@app.post("/process")
async def process_meeting(request: TranscriptRequest):
    try:
        # Extrae el Markdown usando el nuevo prompt optimizado
        result_md = await extract_structured_minutes(request.transcript)
        
        # Gestión de archivos
        base_dir = os.path.dirname(os.path.abspath(__file__))
        doc_dir = os.path.join(base_dir, "..", "doc")
        os.makedirs(doc_dir, exist_ok=True)
        
        filename = f"minuta_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(doc_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result_md)
        
        return {
            "status": "success",
            "file_saved": filename,
            "rawMarkdown": result_md
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-doc")
async def process_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un .docx")
    
    try:
        content = await file.read()
        doc = docx.Document(io.BytesIO(content))
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        transcript = "\n".join(full_text)
        
        if not transcript:
             raise HTTPException(status_code=400, detail="El documento está vacío.")
             
        result_md = await extract_structured_minutes(transcript)
        
        # Guardado del archivo generado desde DOCX
        base_dir = os.path.dirname(os.path.abspath(__file__))
        doc_dir = os.path.join(base_dir, "..", "doc")
        os.makedirs(doc_dir, exist_ok=True)
        
        filename = f"minuta_docx_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(doc_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result_md)
        
        return {
            "status": "success",
            "file_saved": filename,
            "rawMarkdown": result_md
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
