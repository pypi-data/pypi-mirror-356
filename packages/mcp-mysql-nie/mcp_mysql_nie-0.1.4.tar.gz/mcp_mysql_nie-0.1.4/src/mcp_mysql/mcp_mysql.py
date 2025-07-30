from mcp.server.fastmcp import FastMCP
from mcp.server import Server
from contextlib import asynccontextmanager
import mysql.connector
from dotenv import load_dotenv
import os

def get_db_config():
    """从环境变量获取数据库配置信息
    返回:
        dict: 包含数据库连接所需的配置信息
        - host: 数据库主机地址
        - port: 数据库端口
        - user: 数据库用户名
        - password: 数据库密码
        - database: 数据库名称
    异常:
        ValueError: 当必需的配置信息缺失时抛出
    """
 
    # 加载.env文件
    load_dotenv()
 
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
    }
    print(config)
    if not all([config["user"], config["password"], config["database"]]):
        raise ValueError("缺少必需的数据库配置")

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize resources on startup
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    try:
        yield {"conn": conn}
    finally:
        # Clean up on shutdown
        conn.close()

# Pass lifespan to server
mcp = FastMCP("MysqlService", lifespan=server_lifespan)

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