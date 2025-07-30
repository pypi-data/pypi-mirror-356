# 文件名：__main__.py
# 作者：nairoads
# 日期：2025-06-18 15:22:37
# 描述：命令行入口，支持 nairods --help 输出工具说明

import sys

def main():
    help_text = """
Nairods 工具包命令行入口

用法：
    nairods --help         显示本帮助信息
    nairods <tool> ...     运行指定工具（如 feishu, file, time, database 等）

可用工具：
    feishu      飞书API工具
    file        文件/文件夹/Excel/PDF/YAML/ZIP/临时文件工具
    time        时间工具
    database    PostgreSQL数据库工具
    log         日志工具

示例：
    nairods file           查看文件工具说明
    nairods feishu         查看飞书工具说明

详细用法请参考文档或源码注释。
"""
    if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help', 'help'):
        print(help_text)
        return
    tool = sys.argv[1].lower()
    if tool == 'feishu':
        print("飞书API工具：支持消息与图片发送，详见 tools/feishu.py")
    elif tool == 'file':
        print("文件工具：支持文件/文件夹/Excel/PDF/YAML/ZIP/临时文件等操作，详见 tools/file.py")
    elif tool == 'time':
        print("时间工具：常用日期处理，详见 tools/time.py")
    elif tool == 'database':
        print("数据库工具：PostgreSQL 增删改查，详见 tools/database.py")
    elif tool == 'log':
        print("日志工具：loguru 日志，详见 tools/loggertool.py")
    else:
        print(f"未知工具：{tool}，请用 nairods --help 查看可用工具。")

if __name__ == "__main__":
    main() 