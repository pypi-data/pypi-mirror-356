import asyncio
import json
import subprocess
from splatoon_mcp_server.server import main
import pytest

@pytest.mark.asyncio
async def test_hello_world_tool():
    # 启动服务器进程（捕获 stderr）
    proc = subprocess.Popen(
        ["python", "-m", "splatoon_mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,  # 捕获标准错误
        text=True
    )

    # 构造请求并发送（使用 communicate 自动处理输入输出，设置超时）
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "callTool",
        "params": ["hello_world", {"name": "测试用户"}]
    }
    request_str = json.dumps(request) + "\n"

    try:
        # 等待服务器响应（超时 10 秒）
        stdout, stderr = proc.communicate(input=request_str, timeout=10)
    except subprocess.TimeoutExpired:
        proc.terminate()
        raise AssertionError("服务器响应超时")

    # 打印调试信息
    print("--------- 服务器标准输出 ---------")
    print(stdout)
    print("--------- 服务器标准错误 ---------")
    print(stderr)

    # 解析响应
    if not stdout.strip():
        raise AssertionError("服务器未返回任何响应")
    response_data = json.loads(stdout.strip())

    # 验证响应
    assert "result" in response_data, f"响应中无 result 键，原始响应：{response_data}"
    assert response_data["result"][0]["text"] == "你好，测试用户！"

    # 清理进程
    proc.terminate()