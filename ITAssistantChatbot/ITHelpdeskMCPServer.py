import json
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from mcp.server import MCPServer
from dotenv import load_dotenv

load_dotenv()

SEED_TICKETS_PATH = Path(__file__).with_name("mcp_tool_data.json")
with SEED_TICKETS_PATH.open(encoding="utf-8") as ticket_file:
    ticket_store = {
        ticket["ticket_id"]: ticket for ticket in json.load(ticket_file)
    }

ticket_lock = threading.Lock()
next_ticket_number = max(
    (int(ticket_id.split("-")[1]) for ticket_id in ticket_store),
    default=100,
) + 1

mcp_server = MCPServer(
    name="IT Helpdesk MCP Server",
    title="IT Helpdesk MCP Server",
    version="1.0.0",
)


@mcp_server.tool()
def create_support_ticket(
    issue: str,
    description: str,
    employee: str = "Employee",
    priority: str = "Medium",
) -> str:
    """Create an in-memory IT support ticket and return its details."""
    global next_ticket_number

    if not issue.strip() or not description.strip():
        raise ValueError("Both issue and description are required.")

    normalized_priority = priority.title()
    if normalized_priority not in {"Low", "Medium", "High"}:
        raise ValueError("Priority must be Low, Medium, or High.")

    with ticket_lock:
        ticket_id = f"IT-{next_ticket_number}"
        next_ticket_number += 1
        ticket = {
            "ticket_id": ticket_id,
            "employee": employee.strip() or "Employee",
            "issue": issue.strip(),
            "description": description.strip(),
            "priority": normalized_priority,
            "status": "Open",
        }
        ticket_store[ticket_id] = ticket

    return json.dumps(ticket)


@mcp_server.tool()
def check_ticket_status(ticket_id: str) -> str:
    """Return the details and current status of an existing ticket."""
    normalized_ticket_id = ticket_id.strip().upper()
    with ticket_lock:
        ticket = ticket_store.get(normalized_ticket_id)

    if ticket is None:
        return f"Ticket {normalized_ticket_id or '(empty ID)'} was not found."
    return json.dumps(ticket)


mcp_app = mcp_server.streamable_http_app()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _ = _app
    async with mcp_app.router.lifespan_context(mcp_app):
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", mcp_app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
