#!/usr/bin/env python3
"""Test MCP protocol handshake with the Azure Pricing MCP Server."""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path


async def test_mcp_handshake():
    """Test the complete MCP protocol handshake."""
    
    print("=== MCP Protocol Handshake Test ===")
    
    # Set up environment for maximum logging
    env = {
        **os.environ,
        'MCP_DEBUG_LOGGING': 'true',
        'MCP_LOG_LEVEL': 'DEBUG',
        'MCP_LOG_FORMAT': 'json',
        'MCP_LOG_FILE': './logs/mcp-handshake-test.log',
        'FASTMCP_LOG_LEVEL': 'DEBUG',
        'DEFAULT_CURRENCY': 'USD',
        'DEFAULT_REGION': 'eastus'
    }
    
    # Start the server process
    script_path = Path(__file__).parent / "start_server.sh"
    project_root = Path(__file__).parent.parent
    
    print(f"Starting server from: {project_root}")
    print(f"Using script: {script_path}")
    print(f"Log file: {project_root}/logs/mcp-handshake-test.log")
    
    process = None
    try:
        # Start the server process
        process = subprocess.Popen(
            [str(script_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(project_root),
            env=env,
            text=True,
            bufsize=0
        )
        
        print(f"✅ Server process started, PID: {process.pid}")
        
        # Give the server time to start
        print("⏳ Waiting for server to initialize...")
        await asyncio.sleep(3)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Server process exited early with code: {process.returncode}")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return
        
        print("✅ Server process is running")
        
        # Test 1: Initialize request
        print("\n=== Test 1: Initialize Request ===")
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        success = await send_and_receive(process, initialize_request, "initialize")
        if not success:
            return
        
        # Test 2: Tools list request
        print("\n=== Test 2: Tools List Request ===")
        tools_list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        success = await send_and_receive(process, tools_list_request, "tools/list")
        if not success:
            return
        
        # Test 3: Call a specific tool
        print("\n=== Test 3: Tool Call Request ===")
        tool_call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "validate_azure_region",
                "arguments": {
                    "region": "eastus"
                }
            }
        }
        
        success = await send_and_receive(process, tool_call_request, "tools/call")
        
        print("\n=== MCP Handshake Test Complete ===")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if process and process.poll() is None:
            print("\n🧹 Terminating server process...")
            process.terminate()
            try:
                await asyncio.wait_for(asyncio.create_task(asyncio.to_thread(process.wait)), timeout=5)
            except asyncio.TimeoutError:
                print("⚠️  Process didn't terminate gracefully, killing...")
                process.kill()
                process.wait()
    
    # Check log file
    await check_log_file(project_root / "logs" / "mcp-handshake-test.log")


async def send_and_receive(process, request, request_name):
    """Send a request and wait for response."""
    try:
        request_json = json.dumps(request) + '\n'
        print(f"📤 Sending {request_name} request:")
        print(f"   {json.dumps(request, indent=2)}")
        
        # Send the request
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Wait for response with timeout
        print("⏳ Waiting for response...")
        
        response_line = await asyncio.wait_for(
            asyncio.create_task(asyncio.to_thread(process.stdout.readline)),
            timeout=15.0
        )
        
        if response_line.strip():
            print(f"📥 Response received:")
            try:
                response_data = json.loads(response_line)
                print(f"   {json.dumps(response_data, indent=2)}")
                
                # Check response
                if response_data.get('id') == request['id']:
                    if 'result' in response_data:
                        print(f"✅ {request_name} successful!")
                        
                        # Special handling for tools/list
                        if request_name == "tools/list" and 'tools' in response_data['result']:
                            tools = response_data['result']['tools']
                            print(f"📋 Available tools ({len(tools)}):")
                            for tool in tools[:5]:  # Show first 5 tools
                                print(f"   - {tool.get('name', 'unnamed')}: {tool.get('description', 'no description')[:60]}...")
                        
                        return True
                    elif 'error' in response_data:
                        print(f"❌ {request_name} error: {response_data['error']}")
                        return False
                else:
                    print(f"⚠️  Response ID mismatch: expected {request['id']}, got {response_data.get('id')}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON response: {e}")
                print(f"   Raw response: {response_line.strip()}")
                return False
        else:
            print("❌ No response received")
            return False
            
    except asyncio.TimeoutError:
        print(f"❌ Timeout waiting for {request_name} response")
        return False
    except Exception as e:
        print(f"❌ Error during {request_name}: {e}")
        return False


async def check_log_file(log_file_path):
    """Check and display log file contents."""
    print(f"\n=== Log File Analysis ===")
    
    if log_file_path.exists():
        print(f"📄 Log file: {log_file_path}")
        
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
        
        print(f"📊 Total log entries: {len(lines)}")
        
        # Analyze log entries
        startup_logs = []
        request_logs = []
        response_logs = []
        error_logs = []
        
        for line in lines:
            try:
                log_entry = json.loads(line.strip())
                level = log_entry.get('level', '')
                message = log_entry.get('message', '')
                
                if 'Starting' in message or 'configured' in message:
                    startup_logs.append(log_entry)
                elif 'MCP Request' in message:
                    request_logs.append(log_entry)
                elif 'MCP Response' in message:
                    response_logs.append(log_entry)
                elif level == 'ERROR':
                    error_logs.append(log_entry)
                    
            except json.JSONDecodeError:
                continue
        
        print(f"📈 Log breakdown:")
        print(f"   - Startup logs: {len(startup_logs)}")
        print(f"   - Request logs: {len(request_logs)}")
        print(f"   - Response logs: {len(response_logs)}")
        print(f"   - Error logs: {len(error_logs)}")
        
        if error_logs:
            print(f"\n❌ Recent errors:")
            for error in error_logs[-3:]:  # Show last 3 errors
                print(f"   {error.get('timestamp', '')}: {error.get('message', '')}")
        
        if request_logs:
            print(f"\n📤 Recent requests:")
            for req in request_logs[-3:]:  # Show last 3 requests
                print(f"   {req.get('timestamp', '')}: {req.get('message', '')}")
        
        if response_logs:
            print(f"\n📥 Recent responses:")
            for resp in response_logs[-3:]:  # Show last 3 responses
                print(f"   {resp.get('timestamp', '')}: {resp.get('message', '')}")
        
        # Show last few log entries
        print(f"\n📝 Last 5 log entries:")
        for line in lines[-5:]:
            try:
                log_entry = json.loads(line.strip())
                timestamp = log_entry.get('timestamp', '')[:19]  # Truncate timestamp
                level = log_entry.get('level', '')
                message = log_entry.get('message', '')[:80]  # Truncate message
                print(f"   [{timestamp}] {level}: {message}")
            except json.JSONDecodeError:
                print(f"   {line.strip()}")
    else:
        print(f"❌ Log file not found: {log_file_path}")


if __name__ == "__main__":
    asyncio.run(test_mcp_handshake())
