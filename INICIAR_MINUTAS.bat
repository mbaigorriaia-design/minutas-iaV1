@echo off
echo =========================================
echo Iniciando Minutas-IA V1 (Modo Alta Velocidad)
echo =========================================

echo 1. Encendiendo el Cerebro Backend (FastAPI en Puerto 8000)...
cd backend
start cmd /k ".\.venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"
cd ..

echo 2. Encendiendo la Interfaz Visual (Vite en Puerto 5173)...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo !Todo Listo! El sistema se esta abriendo en ventanas separadas.
echo Cierra las ventanas negras cuando quieras apagar la Inteligencia Artificial.
pause
