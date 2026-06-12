@echo off
title NotebookLM MCP Server launcher
echo ===================================================
echo   AVVIATORE SERVER MCP NOTEBOOKLM PER CLAUDE WEB   
echo ===================================================
echo.

cd /d "%~dp0"

echo 1. Verifica della sessione Google...
.venv\Scripts\notebooklm --quiet list > NUL 2> NUL
if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================================================
    echo   ATTENZIONE: LA SESSIONE DI GOOGLE E' SCADUTA O NON VALIDA
    echo ==========================================================
    echo.
    echo Per avviare il connettore, e' necessario accedere a Google.
    echo Premi un tasto per aprire la finestra di login...
    pause
    echo.
    echo Accesso in corso... Per favore, effettua il login nella
    echo finestra del browser che si sta aprendo, poi chiudila.
    echo.
    call .venv\Scripts\notebooklm login
    echo.
    echo Verifica nuovamente la sessione...
    .venv\Scripts\notebooklm --quiet list > NUL 2> NUL
    if %ERRORLEVEL% neq 0 (
        echo.
        echo Errore: l'autenticazione non e' andata a buon fine.
        echo Chiudi questa finestra e riprova ad avviare il file batch.
        pause
        exit /b 1
    )
)

echo Sessione Google verificata con successo!
echo.

:: NOTA: Su Windows, i browser moderni come Brave, Chrome ed Edge bloccano la decrittazione dei cookie da programmi esterni.
:: Per questo motivo il rinnovo automatico silenzioso non puo' funzionare con Brave.
:: set NOTEBOOKLM_REFRESH_CMD="%~dp0.venv\Scripts\notebooklm.exe" login --browser-cookies brave

echo 2. Avvio del server MCP in corso...
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
