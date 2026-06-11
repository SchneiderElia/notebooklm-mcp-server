@echo off
title NotebookLM MCP Server launcher
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
echo 2. Avvio del tunnel pubblico (localhost.run) in corso...
echo    Copia l'indirizzo HTTPS generato nella finestra del tunnel
echo    e inseriscilo come URL del connettore su claude.ai.
echo.
start "localhost.run Tunnel" cmd /k "ssh -R 80:127.0.0.1:8000 nokey@localhost.run"

echo.
echo Launcher completato. Controlla le due finestre che si sono aperte!
echo.
pause
