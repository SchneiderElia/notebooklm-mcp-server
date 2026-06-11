import asyncio
from notebooklm import NotebookLMClient

async def main():
    print("Testing NotebookLM Consumer Client...")
    try:
        # Load credentials from the default storage profile
        async with NotebookLMClient.from_storage() as client:
            print("Successfully connected to NotebookLM!")
            notebooks = await client.notebooks.list()
            print(f"Found {len(notebooks)} notebooks:")
            for nb in notebooks:
                print(f"- {nb.title} (ID: {nb.id}, Sources: {nb.sources_count})")
    except Exception as e:
        print("\nError during test execution:")
        print(f"Exception details: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure you have authenticated by running the login command in your terminal:")
        print("   .venv\\Scripts\\notebooklm login")
        print("2. If you are using Google Chrome, you can authenticate silently by running:")
        print("   .venv\\Scripts\\notebooklm login --browser-cookies chrome")

if __name__ == "__main__":
    asyncio.run(main())
