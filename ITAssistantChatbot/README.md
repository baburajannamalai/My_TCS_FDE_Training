# IT Helpdesk Assistant

## Setup

Install the dependencies from this directory:

```powershell
python -m pip install -r requirements.txt
```

Set `ANTHROPIC_API_KEY` in the environment or in a local `.env` file. The FAQ
is indexed into a local Chroma database on first use; Chroma downloads its
default embedding model the first time it is needed. Web search requires an
internet connection. To start from the provided environment template:

```powershell
Copy-Item .env.example .env
```

In the Streamlit sidebar, upload a UTF-8 `.txt` file (up to 2 MB) to include
its content in retrieval. Uploaded text is indexed for the current chat session
and can be replaced or removed with the uploader.

## Run

Start the MCP ticket server in one terminal:

```powershell
python .\ITHelpdeskMCPServer.py
```

Start the Streamlit app in another terminal:

```powershell
streamlit run .\ITAssistantChatbot.py
```

The app connects to `http://127.0.0.1:8000/mcp` by default. Set
`IT_HELPDESK_MCP_URL` to override that URL. Ticket records are kept in memory
by the MCP server and are reset when it restarts; the sample tickets in
`mcp_tool_data.json` are loaded at startup.
