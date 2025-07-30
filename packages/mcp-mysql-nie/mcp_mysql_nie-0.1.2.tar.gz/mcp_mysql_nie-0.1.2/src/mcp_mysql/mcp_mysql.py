from mcp.server.fastmcp import FastMCP
import mysql.connector
from dotenv import load_dotenv
from mcp.server import Server
import os
from contextlib import asynccontextmanager

load_dotenv()  # 从 .env 加载环境变量

mcp = FastMCP("MysqlService")

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize resources on startup
    conn = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database")
        )
    try:
        yield {"conn": conn}
    finally:
        # Clean up on shutdown
        conn.close()


# Pass lifespan to server
server = Server("example-server", lifespan=server_lifespan)

@mcp.tool()
def execute_query(query: str) -> str:
    """执行 SQL 查询"""
    try:
        ctx = server.request_context
        conn = ctx.lifespan_context["conn"]
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return {"columns": columns, "rows": results}
    except mysql.connector.Error as err:
        return f"查询失败: {err}"
    finally:
        cursor.close()

@mcp.tool()
def list_tables() -> str:
    """列出当前数据库中的所有表"""
    try:
        ctx = server.request_context
        conn = ctx.lifespan_context["conn"]
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except mysql.connector.Error as err:
        return f"获取表列表失败: {err}"
    finally:
        cursor.close()

@mcp.tool()
def describe_table(table_name: str) -> str:
    """描述指定表的结构"""
    try:
        ctx = server.request_context
        conn = ctx.lifespan_context["conn"]
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        description = cursor.fetchall()
        return [{"Field": row[0], "Type": row[1], "Null": row[2], "Key": row[3], "Default": row[4], "Extra": row[5]} for row in description]
    except mysql.connector.Error as err:
        return f"获取表描述失败: {err}"
    finally:
        cursor.close()

def main():
    """主函数，启动 MCP 服务器"""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()