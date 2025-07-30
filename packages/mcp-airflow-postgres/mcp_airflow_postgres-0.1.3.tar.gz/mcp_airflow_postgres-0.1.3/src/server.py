from fastmcp import FastMCP
import os
mcp = FastMCP("mcp-airflow-postgres",
               instructions="This server provides airflow postgresql database tools")


@mcp.tool()
async def failed_runs(start_time, end_time, include_exceed_max_tries:bool=False) -> list:
    """get failed job runs with execution date between start_time and end_time"""
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    # Create a database connection, get connection string from environment variable
    engine = create_engine(os.environ["DATABASE_URL"])        
    
    Session = sessionmaker(bind=engine)
    session = Session()    # Query the database for failed runs
    if include_exceed_max_tries:
        query = text(
            """
            SELECT DISTINCT dr.dag_id, dr.run_id, dr.execution_date, dr.state
            FROM dag_run dr
            JOIN task_instance ti ON dr.dag_id = ti.dag_id AND dr.run_id = ti.run_id
            WHERE dr.execution_date BETWEEN :start_time AND :end_time
            AND (
                dr.state = 'failed' 
                or (
                    ti.try_number > ti.max_tries AND ti.try_number > 0
                )
            )
            """
        )
    else:
        query = text(
            """
            SELECT dag_id, run_id, execution_date, state
            FROM dag_run
            WHERE state = 'failed' AND execution_date BETWEEN :start_time AND :end_time
            """
        )
    result = session.execute(query, {"start_time": start_time, "end_time": end_time})
    failed_runs = result.fetchall()

    # Close the session
    session.close()

    # return LLM-friendly output:
    # [{"dag_id": "dag_id", "run_id": "run_id", "execution_date": "execution_date", "state": "state"}]
    failed_runs = [
        {"dag_id": row[0], "run_id": row[1], "execution_date": row[2], "state": row[3]}
        for row in failed_runs
    ]
    return failed_runs

@mcp.tool()
async def query(query_text) -> list:
    """execute sql query if other tools are not enough"""
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    # Create a database connection, get connection string from environment variable
    engine = create_engine(os.environ["DATABASE_URL"])
    # e.g: engine = create_engine("postgresql://airflow:airflow123@localhost:5432/airflow")
        
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the database for failed runs
    result = session.execute(text(query_text))
    rows = result.fetchall()

    # Close the session
    session.close()

    # return LLM-friendly output:
    rows = [
        {column: row[column] for column in row.keys()}
        for row in rows
    ]
    return rows

# mcp_airflow_postgres/server.py
def main():
    mcp.run()

if __name__ == "__main__":
    main()
