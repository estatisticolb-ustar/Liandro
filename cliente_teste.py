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
            tools = [t.name for t in tools_resp.tools]

            criar_result = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            criar_text = criar_result.content[0].text if criar_result.content else "{}"
            criar_resultado = json.loads(criar_text)

            listar_result = await session.call_tool("listar_tarefas", {})
            listar_text = listar_result.content[0].text if listar_result.content else "[]"
            listar_resultado = json.loads(listar_text)

            saida = {
                "tools": tools,
                "criar_resultado": criar_resultado,
                "listar_resultado": listar_resultado,
            }
            print(json.dumps(saida, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
