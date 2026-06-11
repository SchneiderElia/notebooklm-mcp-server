@echo off
title NotebookLM MCP Server launcher (ngrok)
echo ===================================================
echo   AVVIATORE SERVER MCP NOTEBOOKLM PER CLAUDE WEB   
echo ===================================================
echo.

cd /d "%~dp0"

:: Configura il comando per il refresh automatico e silenzioso dei cookie da Brave.
:: Se usi Chrome, Edge o Firefox, puoi cambiare "brave" in "chrome", "msedge" o "firefox".
set NOTEBOOKLM_REFRESH_CMD="%~dp0.venv\Scripts\notebooklm.exe" login --browser-cookies brave

echo 1. Avvio del server MCP in corso...
start "NotebookLM MCP Server" cmd /k ".venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo.
echo 2. Avvio del tunnel statico ngrok...
echo    L'indirizzo fisso configurato e': https://conceded-job-confess.ngrok-free.dev/mcp
echo.
start "ngrok Tunnel" cmd /k "npx ngrok http --url=conceded-job-confess.ngrok-free.dev 127.0.0.1:8000"

echo.
echo Launcher completato. Controlla le due finestre che si sono aperte!
echo.
pause
