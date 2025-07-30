from mcp.server.fastmcp import FastMCP
import mysql.connector

mcp = FastMCP("MysqlService")
contexts = {"db_connection": None}

@mcp.tool()
def connect_db(host: str, user: str, password: str, database: str) -> str:
    """连接到 MySQL 数据库"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        contexts["db_connection"] = conn
        return "连接成功"
    except mysql.connector.Error as err:
        return f"连接失败: {err}"

@mcp.tool()
def close_connection() -> str:
    """关闭数据库连接"""
    try:
        conn = contexts.get("db_connection")
        if conn:
            conn.close()
            return "连接已关闭"
        else:
            return "没有活动连接"
    except mysql.connector.Error as err:
        return f"关闭连接失败: {err}"

@mcp.tool()
def execute_query(query: str) -> str:
    """执行 SQL 查询"""
    try:
        cursor = contexts.get("db_connection").cursor()
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
        cursor = contexts.get("db_connection").cursor()
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
        cursor = contexts.get("db_connection").cursor()
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