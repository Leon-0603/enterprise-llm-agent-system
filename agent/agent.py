# agent.py

import requests
from router import route_with_confidence

MCP_SERVER_URL = "http://mcp-tools:8000/run"

def call_mcp_tool(tool_name: str, params: dict) -> dict:
    """
    Call MCP Server to execute a tool.
    """
    payload = {
        "tool": tool_name,
        "params": params
    }

    resp = requests.post(MCP_SERVER_URL, json=payload)
    resp.raise_for_status()
    return resp.json()


def agent_run(query: str) -> dict:
    """
    Agent main entry:
    1. Route query
    2. Call MCP tool
    3. Return structured result for UI
    """

    # -------- Step 1: Route --------
    routing = route_with_confidence(query)
    selected_tool = routing["tool"].value
    confidence = routing["confidence"]
    score = {k.value: v for k, v in routing["score"].items()}

    # -------- Step 2: Call Tool --------
    if selected_tool == "rag_tool":
        tool_result = call_mcp_tool(
            tool_name="rag_tool",
            params={"query": query}
        )
    elif selected_tool == "lora_tool":
        tool_result = call_mcp_tool(
            tool_name="lora_tool",
            params={"prompt": query}
        )
    else:
        raise ValueError(f"Unknown tool: {selected_tool}")

    # -------- Step 3: Build Agent Response --------
    return {
        "query": query,
        "selected_tool": selected_tool,
        "confidence": confidence,
        "score": score,
        "tool_output": tool_result.get("output")
    }


# -------- Local test --------
if __name__ == "__main__":
    q = input("User query: ")
    result = agent_run(q)

    print("\n=== Agent Decision ===")
    print("Tool:", result["selected_tool"])
    print("Confidence:", result["confidence"])
    print("Score:", result["score"])

    print("\n=== Output ===")
    print(result["tool_output"])
