#!/usr/bin/env python3
"""Test script to verify MCP protocol communication with the Azure Pricing MCP Server."""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_mcp_server():
    """Test the MCP server by sending basic protocol messages."""
    
    print("=== Azure Pricing MCP Server Protocol Test ===")
    
    # Set up environment
    env = {
        'MCP_DEBUG_LOGGING': 'true',
        'MCP_LOG_LEVEL': 'DEBUG',
        'MCP_LOG_FORMAT': 'json',
        'MCP_LOG_FILE': './logs/protocol-test.log',
        'FASTMCP_LOG_LEVEL': 'DEBUG',
        'DEFAULT_CURRENCY': 'USD',
        'DEFAULT_REGION': 'eastus'
    }
    
    # Start the server process
    script_path = Path(__file__).parent / "start_server.sh"
    project_root = Path(__file__).parent.parent
    
    print(f"Starting server from: {project_root}")
    print(f"Using script: {script_path}")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [str(script_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(project_root),
            env={**env, **dict(os.environ)},
            text=True,
            bufsize=0
        )
        
        print("Server process started, PID:", process.pid)
        
        # Give the server a moment to start
        await asyncio.sleep(2)
        
        # Send initialize request
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
        
        print("Sending initialize request...")
        request_json = json.dumps(initialize_request) + '\n'
        print(f"Request: {request_json.strip()}")
        
        # Send the request
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Wait for response
        print("Waiting for response...")
        
        # Read response with timeout
        try:
            response_line = await asyncio.wait_for(
                asyncio.create_task(asyncio.to_thread(process.stdout.readline)),
                timeout=10.0
            )
            
            if response_line:
                print(f"Response received: {response_line.strip()}")
                try:
                    response_data = json.loads(response_line)
                    print("✅ Valid JSON response received")
                    print(f"Response ID: {response_data.get('id')}")
                    print(f"Response method: {response_data.get('method', 'N/A')}")
                    if 'result' in response_data:
                        print("✅ Initialize successful")
                        print(f"Server capabilities: {response_data['result'].get('capabilities', {})}")
                    elif 'error' in response_data:
                        print(f"❌ Server error: {response_data['error']}")
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON response: {e}")
            else:
                print("❌ No response received")
                
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for response")
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Server process is still running")
        else:
            print(f"❌ Server process exited with code: {process.returncode}")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"Server stderr: {stderr_output}")
        
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if 'process' in locals() and process.poll() is None:
            print("Terminating server process...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    
    # Check log file
    log_file = project_root / "logs" / "protocol-test.log"
    if log_file.exists():
        print(f"\n=== Log File Contents ({log_file}) ===")
        with open(log_file, 'r') as f:
            for line in f:
                print(line.strip())
    else:
        print(f"\n❌ Log file not found: {log_file}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    import os
    asyncio.run(test_mcp_server())
