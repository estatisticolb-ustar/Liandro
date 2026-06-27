import asyncio
import json
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

API_BASE = "http://localhost:8000"

server = Server("servidor-mcp-tarefas")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="criar_tarefa",
            description="Cria uma nova tarefa chamando POST /tarefas na API 4.1.",
            inputSchema={
                "type": "object",
                "properties": {
                    "titulo": {
                        "type": "string",
                        "description": "Titulo da tarefa a ser criada.",
                    }
                },
                "required": ["titulo"],
            },
        ),
        types.Tool(
            name="listar_tarefas",
            description="Lista todas as tarefas chamando GET /tarefas na API 4.1.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10.0) as client:
        if name == "criar_tarefa":
            titulo = arguments.get("titulo", "")
            response = await client.post("/tarefas", json={"titulo": titulo})
            response.raise_for_status()
            resultado = response.json()
        elif name == "listar_tarefas":
            response = await client.get("/tarefas")
            response.raise_for_status()
            resultado = response.json()
        else:
            raise ValueError(f"Tool desconhecida: {name!r}")
    return [types.TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

if __name__ == "__main__":
    asyncio.run(main())
