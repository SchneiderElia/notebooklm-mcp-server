# Google NotebookLM MCP Server for Claude AI

[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-blue.svg)](https://modelcontextprotocol.io/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that connects Google's **NotebookLM** (consumer/free version) directly to **Claude AI (claude.ai)**. This connector allows Claude to interact with your personal NotebookLM notebooks, manage sources, query notes, and generate advanced study guides, audio overviews (podcasts), quizzes, slide decks, and run deep web research.

## 🚀 Configurazione Rapida Automatica con Antigravity 2.0 (Consigliato)

Se stai usando **Antigravity 2.0 (Gemini Coding Assistant)**, non devi fare alcuna installazione manuale! Apri questa cartella di progetto nel tuo IDE, apri la chat di Antigravity e copia-incolla questo prompt:

> **"Configura l'ambiente virtuale di questo progetto, installa i requisiti, installa playwright, fai il login su NotebookLM e registra il server MCP su mcp_config.json"**

L'agente AI farà tutto da solo:
1. Creerà l'ambiente virtuale (`.venv`).
2. Installerà le dipendenze da `requirements.txt`.
3. Installerà i browser per Playwright.
4. Aprirà una finestra del browser per farti fare il login su Google (dovrai solo accedere e chiudere la finestra al termine).
5. Aggiungerà la configurazione dell'MCP server al file `mcp_config.json` globale del tuo IDE.

---

## Features

This server implements the complete set of NotebookLM capabilities, mapping them directly to Claude tools:

* **Notebook Management**: List, create, get details, and delete notebooks.
* **Content Ingestion**: Add raw text documents or web page URLs directly into your notebooks.
* **Interactive Queries**: Query specific notebooks or sources and get grounded answers with citations.
* **Telecontrol (Dashboard) Generation**:
  * **Audio Overview**: Generate podcast-style audio overviews (two-host discussions).
  * **Presentations**: Generate slide deck outlines.
  * **Video Overview**: Create cinematic video summaries.
  * **Mind Maps**: Generate concept maps saved as notes.
  * **Reports & Briefs**: Generate Briefing Documents, Study Guides, Flashcards, Quizzes, Infographics, and Data Tables.
* **Deep Research**: Start deep web searches, compile comprehensive research reports, and automatically import the discovered web sources into your notebook.

## Installation

### Prerequisites

* Python 3.12
* Node.js (for tunneling via ngrok or localtunnel)
* Google Chrome or Edge with a logged-in Google account (for session cookies)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Initialize the Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Install Browser Dependencies**:
   ```bash
   playwright install chromium
   ```

4. **Authenticate**:
   Google NotebookLM does not have an official API, so this connector uses your browser's session cookies.
   
   - **Interactive Login (Default / Brave / Chrome / Edge)**:
     On Windows, Chromium-based browsers (Brave, Chrome, Edge) use App-Bound Encryption, which prevents external scripts from decrypting their cookies. To authenticate:
     ```bash
     .venv\Scripts\notebooklm login
     ```
     This opens a Playwright browser window. Log into your Google account, close the window, and your session will be saved locally.
     
   - **Silent Background Auto-Refresh (Firefox only)**:
     If you have Firefox installed, you can extract cookies silently without interactive prompts. Log into Google on Firefox first, then run:
     ```bash
     .venv\Scripts\notebooklm login --browser-cookies firefox
     ```

## Running the Server

### Option A: Quick Start via Windows Batch Files (Recommended)

If you are on Windows, you can use the pre-configured batch launchers in the root folder:

1. **ngrok Tunnel (Static Domain)**:
   Double-click **`start_notebooklm_mcp_ngrok.bat`**. This will automatically:
   - Check if your Google session is still valid. If it has expired, it prompts you to press a key to run the interactive login browser window.
   - Start the local FastAPI/Starlette MCP server on port `8000`.
   - Start the ngrok tunnel using the configured static domain.
   
   *(Optional: If you use Firefox and want silent auto-refresh, open the batch file and uncomment the `NOTEBOOKLM_REFRESH_CMD` line configured with `firefox`)*.

2. **Alternative Tunnel (localhost.run)**:
   Double-click **`start_notebooklm_mcp.bat`** to start the server with a dynamic `localhost.run` tunnel. It also includes the session verification check.

### Option B: Manual Execution (Command Line)

If you want to run the commands manually:

1. **Set Environment Variable for Silent Auto-Login (Firefox only)**:
   ```cmd
   set NOTEBOOKLM_REFRESH_CMD="path\to\.venv\Scripts\notebooklm.exe" login --browser-cookies firefox
   ```

2. **Start the MCP Server**:
   ```bash
   .venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

3. **Expose with ngrok**:
   ```bash
   ngrok http --url=your-domain.ngrok-free.dev 127.0.0.1:8000
   ```

## Register on Claude Web

1. Go to your **Claude.ai** profile -> **Settings** -> **Developer** -> **Add Custom Connector**.
2. Set the name to **`NotebookLM MCP`** (do *not* use just "NotebookLM" to avoid built-in template conflicts).
3. Insert your tunnel URL: `https://your-domain.ngrok-free.dev/mcp`
4. Leave all OAuth and authentication fields completely empty.
5. Click **Add Connector**.

---

## Register on Antigravity (Gemini Coding Assistant)

You can connect this MCP server directly to **Antigravity / Gemini** to let the AI assistant query your NotebookLM notebooks from any project.

### 💡 The Easy Way (Automated via Chat)
Since Antigravity is a fully agentic coding assistant, you don't need to edit files manually! You can simply ask the assistant in the chat:
> *"Aggiungi il connettore NotebookLM ai miei server MCP"* (or *"Add the NotebookLM connector to my MCP servers"*)

The assistant will automatically locate your `mcp_config.json` file, detect the correct paths for your workspace/virtual environment, and configure the connector for you.

### 🛠️ The Manual Way
If you prefer to configure it manually:

1. Open the Antigravity global MCP configuration file:
   - Path on Windows: `C:\Users\User\.gemini\config\mcp_config.json`
2. Add the `notebooklm` configuration block under `mcpServers`:
   ```json
   "notebooklm": {
     "command": "d:\\nsb\\notebookLM\\.venv\\Scripts\\python.exe",
     "args": [
       "main.py",
       "--stdio"
     ],
     "cwd": "d:\\nsb\\notebookLM"
   }
   ```
   *(Note: Double check that the paths point to your actual project directory and virtual environment, escaping backslashes as `\\`)*.
3. Save the file. Antigravity will automatically reload and enable the NotebookLM tools.

### Example Chat Prompts for Antigravity:
You can now ask the AI assistant to perform actions directly in your chat:
- **List notebooks:** *"Elenca i miei blocchi appunti su NotebookLM"*
- **Query notes:** *"Chiedi a NotebookLM sul blocco appunti 'React' come si gestiscono gli stati"*
- **Add sources:** *"Aggiungi la pagina web https://react.dev come fonte nel blocco appunti 'React'"*
- **Generate Study Guides / Audio Overviews:** *"Genera un documento di sintesi per il blocco appunti 'React'"*

## 📂 Organizzazione in Cartelle e Rinominazione Fonti

### Limite delle Etichette/Cartelle nel Web UI
L'interfaccia web di Google NotebookLM supporta l'auto-etichettatura (Source Labels) per organizzare i file in cartelle. Tuttavia, questa funzionalità è gestita solo a livello visivo sul browser e non viene restituita dalle API di Google. Pertanto, i tool MCP e l'assistente vedranno sempre una lista "piatta" di fonti senza la divisione in cartelle.

### Il Workaround Consigliato
Per fare in modo che la chat e l'MCP riconoscano comunque i tuoi raggruppamenti in cartelle, puoi rinominare le fonti inserendo il nome della categoria come prefisso tra parentesi quadre:
* *Esempio:* Rinomina `WEB_report_aperture-progetti` in `[Web Design] WEB_report_aperture-progetti`.

### Rinominare le Fonti da Chat
Ora puoi rinominare le fonti direttamente dalla chat di Antigravity usando il tool `rename_source`. 
Chiedi semplicemente all'assistente:
> *"Rinomina la fonte [ID-della-fonte] del notebook [ID-del-notebook] in '[Web Design] Nuovo Nome File'"*

*(Nota: puoi recuperare gli ID dei notebook e delle fonti usando i tool `list_notebooks` e `get_notebook_details`)*.

### Risoluzione Problemi: I nuovi tool non compaiono in chat?
Se modifichi il server MCP o aggiorni il codice e l'assistente chat ti dice di non avere a disposizione il tool `rename_source`, significa che l'editor/IDE ha in cache il vecchio processo del server.
* **Come risolvere:** Chiudi completamente l'IDE (VS Code, Cursor, Windsurf, ecc.) e riaprilo, oppure vai nelle impostazioni dei server MCP del tuo IDE e clicca su **"Restart"** o **"Reload"** di fianco al server `notebooklm`.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

*Disclaimer: This is an unofficial connector using automation. Google NotebookLM is a trademark of Google LLC.*
