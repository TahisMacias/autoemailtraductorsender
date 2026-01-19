@echo off
title Iniciar Traductor con ngrok
echo ============================================
echo   Traductor IA + ngrok
echo ============================================
echo.
echo Iniciando servicios:
echo  - Ollama Server (IA)
echo  - n8n (Workflows)
echo  - Servidor Proxy (Web + API)
echo  - ngrok (Acceso desde internet)
echo.

REM Configurar CORS para Ollama
set OLLAMA_ORIGINS=*

REM Detener procesos previos
echo Deteniendo procesos previos...
taskkill /F /IM ollama.exe 2>nul
taskkill /F /IM n8n.exe 2>nul
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Iniciar Ollama
echo [1/4] Iniciando Ollama Server (puerto 11434)...
start "Ollama Server" cmd /k "echo === OLLAMA SERVER === && echo Puerto: 11434 && echo. && ollama serve"
timeout /t 3 /nobreak >nul

REM Iniciar n8n
echo [2/4] Iniciando n8n (puerto 5678)...
start "n8n" cmd /k "echo === N8N === && echo Puerto: 5678 && echo URL: http://localhost:5678 && echo. && n8n start"
timeout /t 5 /nobreak >nul

REM Iniciar servidor proxy
echo [3/4] Iniciando Servidor Proxy (puerto 8080)...
start "Servidor Proxy" cmd /k "echo === SERVIDOR PROXY === && echo Puerto: 8080 && echo Redirige /api/* a Ollama && echo Redirige /webhook/* a n8n && echo. && python servidor-proxy.py"
timeout /t 3 /nobreak >nul

REM Iniciar ngrok
echo [4/4] Iniciando ngrok (puerto 8080)...
start "ngrok" cmd /k "echo === NGROK === && echo. && echo ABRE ESTA URL EN TU NAVEGADOR: && echo. && ngrok http 8080"

echo.
echo ============================================
echo   Servicios iniciados correctamente!
echo ============================================
echo.
echo Como usar:
echo.
echo 1. Busca la ventana "ngrok"
echo 2. Copia la URL (ej: https://xxxx.ngrok-free.app)
echo 3. Abre esa URL en cualquier navegador
echo 4. Listo! El traductor funcionara desde internet
echo.
echo Servicios disponibles:
echo  - Traductor web: https://xxxx.ngrok-free.app
echo  - n8n editor: https://xxxx.ngrok-free.app (abre /n8n en el navegador)
echo  - Ollama API: /api/* (automatico)
echo  - n8n webhooks: /webhook/* (desde workflows)
echo.
echo Para detener: ejecuta detener-servicios.bat
echo.
pause
