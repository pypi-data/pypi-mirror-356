from fastmcp import Client

config = {
    "mcpServers":{
        "mcp-airflow-postgres": {
            "command": "uvx",
            "args": ["--from", "D:\\GPT\\mcp-airflow-postgres", "mcp-airflow-postgres"],
            "env": {
                "DATABASE_URL": "postgresql://airflow:airflow123@localhost:5432/airflow"
            },
            "description": "This server provides airflow postgresql database tools"
        }
    }
}

client = Client(config)

async def main():
    async with client:
        print("Client started")

        tools = await client.list_tools()

        print("Tools available:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        if any(tool.name == "failed_runs" for tool in tools):
            print("Tool 'failed_runs' is available")
            print("Running 'failed_runs' tool...")
            result = await client.call_tool("failed_runs", arguments={"start_time": "2025-05-01T00:00:00", "end_time": "2025-10-31T23:59:59"})
            print("Result:", result)
        if any(tool.name == "query" for tool in tools):
            print("Tool 'query' is available")
            print("Running 'query' tool...")
            result = await client.call_tool("query", arguments={"query_text": "SELECT * FROM dag_run"})
            print("Result:", result)
    # print(f"client is connected:{client.is_connected}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    