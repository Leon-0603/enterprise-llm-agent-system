# agent_server.py
# Agent orchestration layer

from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent_run
import uvicorn

app = FastAPI(title="Agent Server")


class AgentRequest(BaseModel):
    query: str


@app.post("/agent")
def run_agent(req: AgentRequest):
    return agent_run(req.query)


if __name__ == "__main__":
    
    uvicorn.run("agent_server:app", host="0.0.0.0", port=8001, reload=True)
