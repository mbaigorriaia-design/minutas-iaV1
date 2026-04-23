import { useState, useRef } from 'react'
import './index.css'

function App() {
  const [dragActive, setDragActive] = useState(false)
  const [file, setFile] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const inputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.docx') || droppedFile.name.endsWith('.md') || droppedFile.name.endsWith('.txt')) {
        setFile(droppedFile)
        setError(null)
      } else {
        setError("Formato no soportado. Por favor, sube un documento Word (.docx) o texto plano.")
      }
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const abortControllerRef = useRef(null)

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
  }

  const handleUpload = async () => {
    if (!file) return;
    setIsProcessing(true);
    setError(null);
    setResult(null);

    abortControllerRef.current = new AbortController()

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/process-doc", {
        method: "POST",
        body: formData,
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) {
        throw new Error("El servidor falló al procesar el archivo.");
      }

      const data = await response.json();
      
      setResult({
        titulo: "Minuta de Reunión Creada",
        mensaje: "¡Excelente! La IA ha procesado tu documento. El original está en /doc, pero puedes descargarlo aquí mismo.",
        rawData: data.reunion
      });
    } catch (err) {
        if (err.name === 'AbortError') {
            setError("Proceso detenido manualmente.");
        } else {
            console.error(err);
            setError("Hubo un error al conectar con el cerebro de Inteligencia Artificial en el puerto 8000. ¿Está prendido?");
        }
    } finally {
      setIsProcessing(false);
    }
  }

  const downloadMarkdown = () => {
    if (!result) return;
    let md = "";
    
    // Si viene crudo del servidor (Nueva versión rápida)
    if (result.rawMarkdown) {
        md = result.rawMarkdown;
    } else if (result.rawData) {
        // Fallback antiguo si alguien usara la API Pydantic antigua
        const m = result.rawData;
        md = `# ${m.titulo}\n\n**Fecha:** ${m.fecha}\n\n## Resumen Ejecutivo\n${m.resumen_ejecutivo}\n\n`;
        // ... (código existente simplificado, pero el fallback queda)
    }

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `minuta_${new Date().toISOString().replace(/[:.]/g, '')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="app-container">
      <header>
        <h1>Minutas-IA V1</h1>
        <p>Motor Local-First de Inteligencia Artificial para documentación aeroespacial y corporativa</p>
      </header>

      <main className="glass-panel">
        {!result ? (
          <>
            <div 
              className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => inputRef.current?.click()}
            >
              <div className="upload-icon">📄</div>
              <div className="upload-text">
                {file ? file.name : "Arrastra tu documento de reunión aquí"}
              </div>
              <div className="upload-subtext">
                {file ? "Haz clic para procesar la minuta" : "Soporta formatos .docx y texto plano"}
              </div>
              <input 
                ref={inputRef}
                type="file" 
                accept=".docx,.doc,.txt,.md" 
                onChange={handleChange} 
                style={{ display: "none" }} 
              />
            </div>

            {error && (
              <div style={{ color: '#ff6b6b', marginTop: '1rem', textAlign: 'center' }}>
                ⚠️ {error}
              </div>
            )}

            {!isProcessing ? (
              <button 
                className="btn-primary" 
                onClick={handleUpload}
                disabled={!file}
              >
                Generar Minuta Estructurada
              </button>
            ) : (
              <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                <p style={{ color: 'var(--text-muted)' }}>La IA está extrayendo información, leyendo requerimientos y calculando riesgos locales...</p>
                <div className="loading-pulse">
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                </div>
                <button 
                    className="btn-cancel" 
                    onClick={handleCancel}
                    style={{ marginTop: '1.5rem' }}
                >
                    Detener Procesamiento (Abortar)
                </button>
              </div>
            )}
           </>
        ) : (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>✨</div>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>{result.titulo}</h2>
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>{result.mensaje}</p>
            
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <button className="btn-success" onClick={downloadMarkdown}>
                ⬇️ Descargar archivo .md
              </button>
              <button className="btn-primary" onClick={() => { setResult(null); setFile(null); }}>
                Procesar otro documento
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
