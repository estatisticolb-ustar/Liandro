import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = Path(__file__).parent / "servidor_mcp.py"

async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
        env=None,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_resp = await session.list_tools()
            print("=== Tools disponíveis ===")
            for tool in tools_resp.tools:
                print(f"  • {tool.name}: {tool.description}")
            print()

            titulos = ["Estudar MCP", "Implementar API 4.1", "Revisar FastAPI"]
            print("=== Criando tarefas ===")
            for titulo in titulos:
                result = await session.call_tool("criar_tarefa", {"titulo": titulo})
                envelope = {
                    "tool": "criar_tarefa",
                    "arguments": {"titulo": titulo},
                    "content": [
                        {"type": c.type, "text": c.text}
                        for c in result.content
                        if hasattr(c, "text")
                    ],
                    "isError": result.isError,
                }
                print(json.dumps(envelope, ensure_ascii=False, indent=2))
                print()

            print("=== Listando tarefas ===")
            result = await session.call_tool("listar_tarefas", {})
            envelope = {
                "tool": "listar_tarefas",
                "arguments": {},
                "content": [
                    {"type": c.type, "text": c.text}
                    for c in result.content
                    if hasattr(c, "text")
                ],
                "isError": result.isError,
            }
            print(json.dumps(envelope, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
