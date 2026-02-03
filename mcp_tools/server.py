# server.py
# MCP Tool server

import json
import uvicorn
import importlib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback

app = FastAPI(title="MCP Server")

# Load all tool specs from /specs
import os
SPEC_DIR = "specs"
TOOLS = {}

for filename in os.listdir(SPEC_DIR):
    if filename.endswith(".json"):
        path = os.path.join(SPEC_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            spec = json.load(f)

        tool_name = spec["name"]
        TOOLS[tool_name] = spec

print(f"[MCP] Loaded tools: {list(TOOLS.keys())}")


class MCPRequest(BaseModel):
    tool: str
    params: dict


@app.post("/run")
async def run_tool(req: MCPRequest):
    tool = req.tool
    params = req.params

    if tool not in TOOLS:
        return JSONResponse(
            {"error": f"Unknown tool: {tool}"},
            status_code=400
        )

    spec = TOOLS[tool]
    python_cfg = spec.get("python")

    if not python_cfg:
        return JSONResponse(
            {"error": f"Tool {tool} missing python entry"},
            status_code=500
        )

    entry = python_cfg["entrypoint"].replace(".py", "").replace("/", ".")
    func_name = python_cfg["function"]

    #  Load module / function

    try:
        module = importlib.import_module(f"tools.{entry}")
        func = getattr(module, func_name)
    except Exception as e:
        print(" MCP TOOL LOAD ERROR ")
        traceback.print_exc()
        return JSONResponse(
            {
                "error": "Load error",
                "detail": str(e),
                "type": type(e).__name__,
            },
            status_code=500
        )

    #  Exec tool function

    try:
        output = func(**params)

        if not isinstance(output, dict):
            output = {"result": output}

        return {
            "tool": tool,
            "output": output
        }

    except Exception as e:
        print(" MCP TOOL EXECUTION ERROR ")
        traceback.print_exc()
        return JSONResponse(
            {
                "error": "Execution error",
                "detail": str(e),
                "type": type(e).__name__,
            },
            status_code=500
        )

@app.get("/tools")
def list_tools():
    return {"tools": list(TOOLS.keys())}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
