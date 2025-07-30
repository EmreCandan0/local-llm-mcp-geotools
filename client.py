import requests
import json
import ollama
import sys

# MCP server settings
MCP_BASE_URL = "http://127.0.0.1:11435"

# Available tools
AVAILABLE_TOOLS = {
    "analyze_tiff": "Analyzes the TIFF file and returns its metadata",
    "crop_image": "Crops the TIFF file by the given coordinates and converts it to png.",
    "get_ndvi": "Calculates the mean ndvi and given coordinates ndvi."
}

# Add path where MCP functions are located
sys.path.append('/')

def parse_mcp_response(response_text):
    """
    Parses MCP event-stream (SSE) responses as JSON.
    """
    if "data:" in response_text:
        lines = [line for line in response_text.splitlines() if line.startswith("data:")]
        if not lines:
            return None
        json_str = lines[-1][len("data: "):]
        try:
            data = json.loads(json_str)
            return data
        except Exception as e:
            print("JSON parse error:", e)
            return None
    else:
        try:
            return json.loads(response_text)
        except Exception as e:
            print("JSON parse error:", e)
            return None

def call_ollama(prompt):
    """
    Sends the user request to the local Ollama LLM (phi3) and returns raw tool call output.
    """
    try:
        response = ollama.chat(model='phi3', messages=[
            {
                'role': 'user',
                'content': f"""
For any user request, if a tool is needed, ONLY output in this format:

TOOL_NEEDED: tool_name
PARAMS: {{"param1": value1, ...}}

Do NOT output explanations, steps, or code. Only the tool call(s). 

User request: {prompt}
"""
            }
        ])
        return response['message']['content']
    except Exception as e:
        return f"Ollama error: {e}"

def call_mcp_tool(tool_name, params):
    """
    Calls an MCP tool and parses the response (supports event-stream and JSON).
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params
        },
        "id": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    try:
        print(f" Calling MCP tool: {tool_name}")
        resp = requests.post(f"{MCP_BASE_URL}/mcp", json=payload, headers=headers)

        result = parse_mcp_response(resp.text)
        if result is None:
            print(f" Unable to parse MCP response: {resp.text}")
            return None

        if "result" in result:
            return result["result"]
        elif "error" in result:
            return result["error"]
        else:
            return result

    except Exception as e:
        print(f" MCP connection error: {e}")

def parse_phi3_multi_response(response):
    """
    Parses multiple TOOL_NEEDED and PARAMS blocks from phi3's output.
    """
    tool_calls = []
    tool_name = None
    params = None

    lines = response.splitlines()
    for line in lines:
        if line.startswith("TOOL_NEEDED:"):
            tool_name = line.replace("TOOL_NEEDED:", "").strip().strip(",")
        elif line.startswith("PARAMS:"):
            try:
                params_str = line.replace("PARAMS:", "").strip()
                params = json.loads(params_str)
                if tool_name:
                    tool_calls.append((tool_name, params))
                    tool_name = None
            except Exception as e:
                print("PARAMS parse error:", e)
                continue
    return tool_calls

def main():
    print("Assistant started")
    print("MCP Server:", MCP_BASE_URL)
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("➤ Your request: ").strip()

            if user_input.lower() in ['quit', 'exit', 'çık']:
                print("Exiting...")
                break

            if not user_input:
                continue

            print(" Phi3 is analyzing...")
            phi3_response = call_ollama(user_input)
            tool_calls = parse_phi3_multi_response(phi3_response)

            if tool_calls:
                for tool_name, params in tool_calls:
                    if tool_name and tool_name in AVAILABLE_TOOLS:
                        print(f"🔧 Calling tool: {tool_name}...")
                        result = call_mcp_tool(tool_name, params)
                        print(" Result:", json.dumps(result, indent=2, ensure_ascii=False))
                    else:
                        print(f" Unknown or unavailable tool: {tool_name}")
            else:
                print(" Phi3:", phi3_response)

        except Exception as error:
            print(f"\n\nExiting due to error: {error}")
            break
