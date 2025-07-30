必须在powershell中已管理员的身份运行
安装服务
nssm install <servicename> <app> [<args> ...]
nssm install sqlite_mcp_server_8000 D:\root\projects\python\tut-autogen\.venv\Scripts\python.exe D:\root\projects\python\tut-autogen\src\tut_autogen\t10_sqlite_mcp\sqlite_mcp_server.py --db=D:\root\projects\python\tut-langgraph\src\tut_langgraph\t4_sql_agent\student_database.db
删除服务
nssm remove sqlite_mcp_server_8000
安装服务
nssm start sqlite_mcp_server_8000
重启服务
nssm restart sqlite_mcp_server_8000
停止服务
nssm stop sqlite_mcp_server_8000
查看状态
nssm status sqlite_mcp_server_8000
设置日志(需要重启)
nssm set sqlite_mcp_server_8000 AppStdout D:\root\projects\python\tut-autogen\logs\sqlite_mcp_server_8000.log
nssm set sqlite_mcp_server_8000 AppStderr D:\root\projects\python\tut-autogen\logs\sqlite_mcp_server_8000.err
