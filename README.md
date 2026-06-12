# Google NotebookLM MCP Server for Claude AI

[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-blue.svg)](https://modelcontextprotocol.io/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that connects Google's **NotebookLM** (consumer/free version) directly to **Claude AI (claude.ai)**. This connector allows Claude to interact with your personal NotebookLM notebooks, manage sources, query notes, and generate advanced study guides, audio overviews (podcasts), quizzes, slide decks, and run deep web research.

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
   You can authenticate the client by extracting cookies automatically from your browser (e.g., Brave, Chrome, Edge, Firefox):
   ```bash
   .venv\Scripts\notebooklm login --browser-cookies brave
   ```
   *Alternatively, if automatic extraction fails or you prefer an interactive login, run:*
   ```bash
   .venv\Scripts\notebooklm login
   ```
   This will open a browser window for a manual Google login and save the session automatically.

## Running the Server

### Option A: Quick Start via Windows Batch Files (Recommended)

If you are on Windows, you can use the pre-configured batch launchers in the root folder:

1. **ngrok Tunnel (Static Domain)**:
   Double-click **`start_notebooklm_mcp_ngrok.bat`**. This will automatically:
   - Configure `NOTEBOOKLM_REFRESH_CMD` to silently extract cookies from the **Brave** browser when session expires.
   - Start the local FastAPI/Starlette MCP server on port `8000`.
   - Start the ngrok tunnel using the configured static domain.

2. **Alternative Tunnel (localhost.run)**:
   Double-click **`start_notebooklm_mcp.bat`** to start the server with a dynamic `localhost.run` tunnel (useful if you don't have a static ngrok domain).

### Option B: Manual Execution (Command Line)

If you want to run the commands manually:

1. **Set Environment Variable (Optional for silent auto-login)**:
   ```cmd
   set NOTEBOOKLM_REFRESH_CMD="path\to\.venv\Scripts\notebooklm.exe" login --browser-cookies brave
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

*Disclaimer: This is an unofficial connector using automation. Google NotebookLM is a trademark of Google LLC.*
