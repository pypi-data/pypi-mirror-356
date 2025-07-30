from odps import ODPS
from mcp.server.fastmcp import FastMCP
import os

odps = ODPS(
    os.getenv('ALIYUN_ACCESS_KEY_ID'),
    os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
    project=os.getenv('ALIYUN_MAXCOMPUTE_PROJECT_NAME'),
    endpoint=os.getenv('ALIYUN_MAXCOMPUTE_ENDPOINT'),
)


mcp = FastMCP(
    name="MaxcomputeAssistant",
    instructions="maxcompute assistant is a professional MaxCompute data warehouse assistant, helping users run MaxCompute SQL queries.",
)


@mcp.tool(name="run_sql", description="Run a SQL query on the MaxCompute data warehouse.")
def run_sql(sql: str) -> str:
    """
    Run a SQL query on the MaxCompute data warehouse.
    """

    result = []
    with odps.execute_sql(sql).open_reader(tunnel=False) as reader:
        for record in reader.to_result_frame():
            result.append(record)

    print(result[0])
    return result

@mcp.tool(name="list_tables", description="List all tables in the database.")
def list_tables() -> str:
    """
    List all tables in the database.
    """

    tables = []
    for table in odps.list_tables():
        tables.append(table.name)

    return "\n".join(tables)


def main():
    mcp.run(transport="stdio")


