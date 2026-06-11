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

1. **Start the MCP Server**:
   ```bash
   .venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

2. **Expose with ngrok**:
   ```bash
   ngrok http --url=your-domain.ngrok-free.dev 127.0.0.1:8000
   ```

3. **Register on Claude Web**:
   * Go to **Settings** -> **Developer** -> **Add Custom Connector**.
   * Name: `NotebookLM MCP`
   * URL: `https://your-domain.ngrok-free.dev/mcp`
   * Leave authentication fields empty.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

*Disclaimer: This is an unofficial connector using automation. Google NotebookLM is a trademark of Google LLC.*
