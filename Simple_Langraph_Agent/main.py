import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

app = FastAPI(
    title="Dynamic Agent API",
    description="FastAPI wrapper around the LangChain agent with weather, post, and daily thought tools.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


def get_post(post_id: int) -> str:
    """Get post details from JSONPlaceholder using a post ID."""
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return "Post not found"
    post = response.json()
    return (
        f"Post ID: {post['id']}\n"
        f"Title: {post['title']}\n\n"
        f"Body:\n{post['body']}"
    )


def create_daily_thought() -> str:
    """Generate an inspirational daily thought using the LLM."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(
        "Generate a short, unique inspirational daily thought in one or two sentences."
    )
    return response.content


# ---------------------------------------------------------------------------
# Agent (initialised once at startup)
# ---------------------------------------------------------------------------

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, create_daily_thought, get_post],
    system_prompt="You are a helpful assistant",
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AgentRequest(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {"message": "What's the weather in Hyderabad?"}
        }
    }


class AgentResponse(BaseModel):
    reply: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint."""
    return {"status": "ok", "message": "Agent API is running."}


@app.post("/agent", response_model=AgentResponse, tags=["Agent"])
def run_agent(request: AgentRequest):
    """
    Send a message to the agent and receive its reply.

    The agent has access to:
    - **get_weather(city)** – returns a sunny forecast for any city
    - **get_post(post_id)** – fetches a post from JSONPlaceholder
    - **create_daily_thought()** – generates an inspirational thought via GPT-4o-mini
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message must not be empty.")

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]}
        )
        reply = result["messages"][-1].content
        return AgentResponse(reply=reply)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
