from fastmcp import FastMCP
import sqlite3
from typing import List, Dict, Any
import os
import argparse
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from loguru import logger

mcp = FastMCP("SQLiteMCP")

# 设置数据库路径并验证
DB_PATH = None


# 资源：获取数据库模式
@mcp.resource("schema://main")
def get_schema() -> str:
    """提供 SQLite 数据库的表模式信息"""
    try:
        logger.debug(f"正在获取数据库模式，数据库路径: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        schemas = cursor.fetchall()
        conn.close()
        logger.debug(f"成功获取 {len(schemas)} 个表的模式")
        return "\n".join(sql[0] for sql in schemas if sql[0])
    except Exception as e:
        return f"获取模式失败: {str(e)}"


# 工具：列出所有表
@mcp.tool()
def list_tables() -> List[str]:
    """返回数据库中的所有表名"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        logger.debug(f"成功获取表列表，共 {len(tables)} 个表: {tables}")
        conn.close()
        return tables
    except Exception as e:
        logger.exception(f"获取表列表失败: {e}")
        return {"error": f"获取表列表失败: {str(e)}"}


# 工具：描述表结构
@mcp.tool()
def describe_table(table_name: str) -> List[Dict[str, Any]]:
    """返回指定表的列信息（名称、类型、约束等）"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [
            {"name": row[1], "type": row[2], "not_null": bool(row[3]), "primary_key": bool(row[5])}
            for row in cursor.fetchall()
        ]
        conn.close()
        if not columns:
            return {"error": f"表 {table_name} 不存在"}
        logger.debug(f"成功获取表 {table_name} 的结构，共 {len(columns)} 列")
        return columns
    except Exception as e:
        return {"error": f"描述表失败: {str(e)}"}


# 工具：执行安全的 SELECT 查询
@mcp.tool()
def query_data(sql: str) -> List[Dict[str, Any]]:
    """执行 SELECT 查询并返回结果"""
    if not sql.strip().upper().startswith("SELECT"):
        return {"error": "仅支持 SELECT 查询以确保安全性"}
    try:
        logger.debug(f"开始执行SQL查询: {sql}")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        logger.debug(f"查询执行成功，返回 {len(results)} 条记录")
        return results
    except Exception as e:
        return {"error": f"查询失败: {str(e)}"}


# 提示模板：生成 SQL 查询
@mcp.prompt()
def generate_sql(description: str, schema: str = None) -> str:
    """根据用户描述和数据库模式生成 SQL 查询"""
    if schema is None:
        schema = mcp.resources["schema://main"].get()
    return f"""
    你是一个 SQL 专家。根据以下数据库模式和用户描述，生成一个正确的 SQL SELECT 查询。

    数据库模式：
    {schema}

    用户描述：
    {description}

    输出：
    - 仅返回 SQL 查询语句，不要包含解释或其他内容。
    - 确保查询是安全的 SELECT 语句。
    """


# 工具：检查表是否存在
@mcp.tool()
def table_exists(table_name: str) -> Dict[str, bool]:
    """检查指定表是否存在"""
    try:
        logger.debug(f"开始检查表是否存在，表名: {table_name}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        exists = bool(cursor.fetchone())
        conn.close()
        logger.debug(f"表 {table_name} 存在状态: {exists}")
        return {"table": table_name, "exists": exists}
    except Exception as e:
        logger.exception(f"检查表 {table_name} 存在状态失败: {e}")
        return {"error": f"检查失败: {str(e)}"}


# 运行服务器
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="SQLite MCP Server")
    parser.add_argument("--db", type=str, required=True, help="Path to SQLite database file")
    parser.add_argument("--port", "-p", type=int, default=18085, help="Port for the SSE server")
    args = parser.parse_args()
    DB_PATH = args.db
    logger.debug(f"启动 SQLite MCP 服务器，使用数据库: {DB_PATH}")
    mcp.run(transport="sse", host="0.0.0.0", port=args.port)
