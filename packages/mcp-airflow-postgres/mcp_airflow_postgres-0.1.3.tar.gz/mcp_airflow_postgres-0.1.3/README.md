# MCP Airflow Database

A Model Context Protocol (MCP) server for interacting with Airflow databases.

## Setup with Poetry

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed on your system

### Installation

1. Clone this repository:
   ```powershell
   git clone <your-repository-url>
   cd mcp-airflow-db
   ```

2. Install dependencies with Poetry:
   ```powershell
   poetry install
   ```

3. Configure your environment:
   Create a `.env` file with your database connection string:
   ```
   DATABASE_URL=postgresql://airflow:airflow123@localhost:5432/airflow
   ```

### Running the MCP Server

Run the server with Poetry:
```powershell
poetry run python src/server.py
```

Or activate the Poetry environment first:
```powershell
poetry shell
python src/server.py
```

## Using with Smithery

This MCP can be used with Smithery directly as configured in the `smithery.yaml` file. Make sure to provide the `DATABASE_URL` configuration when starting the server.

## Available Tools

- `failed_runs`: Query failed Airflow DAG runs within a specified time period.
- `query`: Execute SQL queries directly against the Airflow database.

## License

[Your License]
