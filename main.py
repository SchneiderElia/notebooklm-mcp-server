import os
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from notebooklm import NotebookLMClient, ReportFormat

# 1. Define native FastMCP lifespan context manager
@asynccontextmanager
async def mcp_lifespan(server):
    global client
    print("Initializing NotebookLM MCP Server...")
    # Open client session on startup using the default profile with background keepalive (every 10 minutes)
    async with NotebookLMClient.from_storage(keepalive=600) as active_client:
        client = active_client
        print("NotebookLM Client connected.")
        yield
    print("NotebookLM MCP Server shutting down...")

# 2. Initialize FastMCP with lifespan
mcp = FastMCP("NotebookLM MCP Server", lifespan=mcp_lifespan)

# Disable DNS rebinding protection to allow connection via public tunnels (ngrok, localhost.run, etc.)
mcp.settings.transport_security.enable_dns_rebinding_protection = False

# 3. Global client reference managed by lifespan
client = None

def get_client() -> NotebookLMClient:
    if client is None:
        raise RuntimeError(
            "NotebookLM client is not initialized or connected. "
            "Please make sure you have run 'notebooklm login' in your terminal."
        )
    return client

# 3. Define MCP Tools

@mcp.tool()
async def list_notebooks() -> str:
    """List all NotebookLM notebooks in the user's account.
    
    Returns:
        A formatted string listing the notebook titles, IDs, and source counts.
    """
    try:
        c = get_client()
        notebooks = await c.notebooks.list()
        if not notebooks:
            return "No notebooks found in your account."
        
        lines = ["Available Notebooks:"]
        for nb in notebooks:
            lines.append(
                f"- Title: {nb.title}\n"
                f"  Notebook ID: {nb.id}\n"
                f"  Sources Count: {nb.sources_count}\n"
                "  ---"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing notebooks: {str(e)}"

@mcp.tool()
async def create_notebook(title: str) -> str:
    """Create a new NotebookLM notebook.
    
    Args:
        title: The title of the notebook.
        
    Returns:
        Confirmation message with the created notebook ID.
    """
    try:
        c = get_client()
        nb = await c.notebooks.create(title)
        return (
            f"Successfully created notebook:\n"
            f"- Title: {nb.title}\n"
            f"- Notebook ID: {nb.id}"
        )
    except Exception as e:
        return f"Error creating notebook: {str(e)}"

@mcp.tool()
async def get_notebook_details(notebook_id: str) -> str:
    """Get details of a specific NotebookLM notebook, including its sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        Formatted string containing notebook details and list of sources.
    """
    try:
        c = get_client()
        nb = await c.notebooks.get(notebook_id)
        sources = await c.sources.list(notebook_id)
        
        lines = [
            f"Title: {nb.title}",
            f"Notebook ID: {nb.id}",
            f"Sources Count: {len(sources)}",
            "\nSources:"
        ]
        
        if not sources:
            lines.append("  No sources added to this notebook yet.")
        else:
            for s in sources:
                lines.append(
                    f"  - [{s.id}] {s.title or 'Untitled'}\n"
                    f"    URL: {s.url or 'None'}\n"
                    f"    Status: {s.status.name if hasattr(s.status, 'name') else str(s.status)}"
                )
                
        return "\n".join(lines)
    except Exception as e:
        return f"Error getting notebook details: {str(e)}"

@mcp.tool()
async def delete_notebook(notebook_id: str) -> str:
    """Delete a NotebookLM notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        Confirmation message.
    """
    try:
        c = get_client()
        await c.notebooks.delete(notebook_id)
        return f"Successfully deleted notebook: {notebook_id}"
    except Exception as e:
        return f"Error deleting notebook: {str(e)}"

@mcp.tool()
async def add_text_source(notebook_id: str, title: str, content: str) -> str:
    """Add a raw text document source to a NotebookLM notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        title: The title of the source document.
        content: The text content of the document.
        
    Returns:
        Confirmation message.
    """
    try:
        c = get_client()
        await c.sources.add_text(notebook_id, title, content, wait=True)
        return f"Successfully added text source '{title}' to notebook {notebook_id}."
    except Exception as e:
        return f"Error adding text source: {str(e)}"

@mcp.tool()
async def add_web_source(notebook_id: str, url: str) -> str:
    """Add a web page URL source to a NotebookLM notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        url: The URL of the web page to ingest.
        
    Returns:
        Confirmation message.
    """
    try:
        c = get_client()
        # In the consumer API, add_url fetches the page and titles it automatically
        await c.sources.add_url(notebook_id, url, wait=True)
        return f"Successfully added web source ({url}) to notebook {notebook_id}."
    except Exception as e:
        return f"Error adding web source: {str(e)}"

@mcp.tool()
async def rename_source(notebook_id: str, source_id: str, new_title: str) -> str:
    """Rename an existing source inside a NotebookLM notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        source_id: The ID of the source to rename.
        new_title: The new title for the source.
        
    Returns:
        Confirmation message with the renamed source details.
    """
    try:
        c = get_client()
        src = await c.sources.rename(notebook_id, source_id, new_title)
        if src:
            return f"Successfully renamed source to '{src.title}' (ID: {src.id})."
        else:
            return f"Successfully renamed source to '{new_title}'."
    except Exception as e:
        return f"Error renaming source: {str(e)}"

@mcp.tool()
async def query_notebook(notebook_id: str, question: str, source_ids: list[str] = None) -> str:
    """Ask a question to the NotebookLM notebook. It processes all or specific sources and returns a grounded answer with citations.
    
    Args:
        notebook_id: The ID of the notebook.
        question: The question or query to ask.
        source_ids: Optional list of source IDs to restrict the query. If omitted, queries all sources.
        
    Returns:
        The grounded answer from NotebookLM with citations.
    """
    try:
        c = get_client()
        res = await c.chat.ask(notebook_id, question, source_ids)
        
        # Structure formatting for response and citations
        ans_text = res.answer
        
        if res.references:
            ans_text += "\n\nReferences/Citations:"
            for ref in res.references:
                ans_text += f"\n- [{ref.citation_number}] Source ID: {ref.source_id}\n  Snippet: {ref.cited_text}"
                
        return ans_text
    except Exception as e:
        return f"Error querying notebook: {str(e)}"

@mcp.tool()
async def list_artifacts(notebook_id: str) -> str:
    """List all generated artifacts (such as briefing docs, study guides, audio overviews, slide decks, etc.) in the notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        A formatted list of artifacts.
    """
    try:
        c = get_client()
        artifacts = await c.artifacts.list(notebook_id)
        if not artifacts:
            return "No artifacts found in this notebook."
        
        lines = ["Notebook Artifacts:"]
        for a in artifacts:
            lines.append(
                f"- Title: {a.title or 'Untitled'}\n"
                f"  Artifact ID: {a.id}\n"
                f"  Type (Kind): {a.kind.name if hasattr(a.kind, 'name') else str(a.kind)}\n"
                f"  Status: {a.status_str or 'unknown'}\n"
                "  ---"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing artifacts: {str(e)}"

@mcp.tool()
async def get_report_content(notebook_id: str, artifact_id: str) -> str:
    """Get the text (markdown) content of a generated report artifact (Briefing Doc, Study Guide, Blog Post, FAQ, Timeline).
    
    Args:
        notebook_id: The ID of the notebook.
        artifact_id: The ID of the report artifact.
        
    Returns:
        The markdown text content of the report.
    """
    try:
        c = get_client()
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "report.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact_id)
            return content
    except Exception as e:
        return f"Error downloading report content: {str(e)}"

@mcp.tool()
async def generate_briefing_doc(notebook_id: str) -> str:
    """Generate a new Briefing Document artifact from the notebook's sources and return its content.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        The markdown content of the generated Briefing Document.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_report(notebook_id, report_format=ReportFormat.BRIEFING_DOC)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "report.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact.id)
            return f"Briefing Document successfully generated (ID: {artifact.id}):\n\n{content}"
    except Exception as e:
        return f"Error generating Briefing Document: {str(e)}"

@mcp.tool()
async def generate_study_guide(notebook_id: str) -> str:
    """Generate a new Study Guide artifact from the notebook's sources and return its content.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        The markdown content of the generated Study Guide.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_study_guide(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "report.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact.id)
            return f"Study Guide successfully generated (ID: {artifact.id}):\n\n{content}"
    except Exception as e:
        return f"Error generating Study Guide: {str(e)}"

@mcp.tool()
async def generate_quiz(notebook_id: str) -> str:
    """Generate a new interactive Quiz artifact from the notebook's sources and return its content.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        The markdown content of the generated Quiz.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_quiz(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "report.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact.id)
            return f"Quiz successfully generated (ID: {artifact.id}):\n\n{content}"
    except Exception as e:
        return f"Error generating Quiz: {str(e)}"

@mcp.tool()
async def generate_flashcards(notebook_id: str) -> str:
    """Generate new Flashcards from the notebook's sources and return its content.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        The markdown content of the generated Flashcards.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_flashcards(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "report.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact.id)
            return f"Flashcards successfully generated (ID: {artifact.id}):\n\n{content}"
    except Exception as e:
        return f"Error generating Flashcards: {str(e)}"

@mcp.tool()
async def generate_audio_overview(notebook_id: str) -> str:
    """Generate a podcast-style Audio Overview (Audio Overview) from the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        A confirmation message showing the status and artifact details.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_audio(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        return (
            f"Audio Overview successfully generated!\n"
            f"- Artifact ID: {artifact.id}\n"
            f"- Status: {artifact.status_str or 'completed'}\n"
            f"- URL: {artifact.url or 'None'}"
        )
    except Exception as e:
        return f"Error generating Audio Overview: {str(e)}"

@mcp.tool()
async def generate_slide_deck(notebook_id: str, instructions: str = None) -> str:
    """Generate a Slide Deck (Presentation outline) artifact from the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        instructions: Optional special formatting or content instructions for the presentation.
        
    Returns:
        A confirmation message with the generated slide deck details.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_slide_deck(notebook_id, instructions=instructions)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        return (
            f"Slide Deck successfully generated!\n"
            f"- Artifact ID: {artifact.id}\n"
            f"- Status: {artifact.status_str or 'completed'}\n"
            f"- URL: {artifact.url or 'None'}"
        )
    except Exception as e:
        return f"Error generating Slide Deck: {str(e)}"

@mcp.tool()
async def run_deep_research(notebook_id: str, query: str) -> str:
    """Run a Deep Research web search task for a query, wait for it to finish, and ingest the sources and the research report into the notebook.
    
    Args:
        notebook_id: The ID of the notebook.
        query: The search topic or query to research.
        
    Returns:
        The markdown report generated by the Deep Research search.
    """
    try:
        c = get_client()
        task = await c.research.start(notebook_id, query, source="web", mode="fast")
        if not task:
            return "Failed to start Deep Research task."
        
        result = await c.research.wait_for_completion(notebook_id, task.task_id)
        
        status_val = result.status.value if hasattr(result.status, "value") else str(result.status)
        if status_val == "completed":
            await c.research.import_sources(notebook_id, task.task_id, result.sources)
            return (
                f"Deep Research completed successfully and sources have been imported into the notebook!\n\n"
                f"Generated Research Report:\n"
                f"==========================\n"
                f"{result.report or 'No report content generated.'}"
            )
        else:
            return f"Deep Research task finished with status: {status_val}."
    except Exception as e:
        return f"Error running Deep Research: {str(e)}"

@mcp.tool()
async def generate_video_overview(notebook_id: str) -> str:
    """Generate a Video Overview (cinematic overview) from the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        A confirmation message showing the status and artifact details.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_video(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        return (
            f"Video Overview successfully generated!\n"
            f"- Artifact ID: {artifact.id}\n"
            f"- Status: {artifact.status_str or 'completed'}\n"
            f"- URL: {artifact.url or 'None'}"
        )
    except Exception as e:
        return f"Error generating Video Overview: {str(e)}"

@mcp.tool()
async def generate_mind_map(notebook_id: str) -> str:
    """Generate a Mind Map artifact representing the concepts of the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        A confirmation message showing the mind map note details.
    """
    try:
        c = get_client()
        res = await c.artifacts.generate_mind_map(notebook_id)
        return (
            f"Mind Map successfully generated!\n"
            f"- Note ID: {res.note_id or 'None'}\n"
            f"- Details: Mind map has been saved as a note in the notebook."
        )
    except Exception as e:
        return f"Error generating Mind Map: {str(e)}"

@mcp.tool()
async def generate_infographic(notebook_id: str) -> str:
    """Generate an Infographic artifact summarizing the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        A confirmation message with the generated infographic details.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_infographic(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        return (
            f"Infographic successfully generated!\n"
            f"- Artifact ID: {artifact.id}\n"
            f"- Status: {artifact.status_str or 'completed'}\n"
            f"- URL: {artifact.url or 'None'}"
        )
    except Exception as e:
        return f"Error generating Infographic: {str(e)}"

@mcp.tool()
async def generate_data_table(notebook_id: str) -> str:
    """Generate a Data Table artifact summarizing the notebook's sources.
    
    Args:
        notebook_id: The ID of the notebook.
        
    Returns:
        The markdown table content generated.
    """
    try:
        c = get_client()
        status = await c.artifacts.generate_data_table(notebook_id)
        artifact = await c.artifacts.wait_for_completion(notebook_id, status.task_id)
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = os.path.join(tmpdir, "table.md")
            content = await c.artifacts.download_report(notebook_id, temp_path, artifact.id)
            return f"Data Table successfully generated (ID: {artifact.id}):\n\n{content}"
    except Exception as e:
        return f"Error generating Data Table: {str(e)}"


# 4. Starlette / FastMCP App Setup
app = mcp.streamable_http_app()

if __name__ == "__main__":
    import sys
    if "--stdio" in sys.argv:
        mcp.run(transport="stdio")
    else:
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")
        uvicorn.run(app, host=host, port=port)
