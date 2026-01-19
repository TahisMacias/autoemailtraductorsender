@echo off
title Detener Servicios
echo ============================================
echo   Deteniendo servicios del traductor
echo ============================================
echo.

echo [1/4] Deteniendo Ollama...
taskkill /F /IM ollama.exe >nul 2>&1

echo [2/4] Deteniendo n8n...
taskkill /F /IM n8n.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

echo [3/4] Deteniendo Servidor Proxy...
taskkill /F /IM python.exe >nul 2>&1

echo [4/4] Deteniendo ngrok...
taskkill /F /IM ngrok.exe >nul 2>&1

echo.
echo ============================================
echo   Todos los servicios detenidos!
echo ============================================
echo.
pause
