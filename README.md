# Simple LangChain Agent with Evaluation

A production-ready AI agent built with LangChain and LangGraph that demonstrates dynamic tool use with OpenAI models. Includes built-in evaluation and testing via LangSmith for validating agent behavior.

## Features

- 🌤️ **Weather Tool** – Retrieve weather information for any city
- 💡 **Daily Thought Tool** – Generate unique, inspirational thoughts using GPT-4o-mini
- 🤖 **Dynamic Agent** – Powered by GPT-4o, handles tool selection and invocation automatically
- 📊 **LangSmith Integration** – Trace agent executions and evaluate performance with custom evaluators
- ✅ **Comprehensive Testing** – Built-in evaluation suite with exact-match and LLM-judge evaluators

## Prerequisites

- Python 3.9+
- OpenAI API Key
- LangSmith API Key (optional, for evaluation and tracing)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alumnx-ai-labs/Ai_Agent.git
cd Ai_Agent/Simple_Langraph_Agent
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example `.env` file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=your_project_name_here
```

**Note:** The LANGSMITH_* variables are optional. If you don't provide them, the agent will still work but won't log traces to LangSmith.

## Usage

### Running the Agent

Execute the agent with a user message:

```bash
# Query the weather tool
python dynamic_agent_input.py "What's the weather in Hyderabad?"

# Request an inspirational thought
python dynamic_agent_input.py "Give me an inspirational thought for today"

# Multi-part requests
python dynamic_agent_input.py "Tell me the weather in Mumbai and share a daily thought"
```

The agent will:
1. Analyze your input
2. Determine which tools to use (if any)
3. Invoke the appropriate tools
4. Return only the result without additional commentary

### Running Evaluations

Evaluate agent performance against a test dataset:

```bash
python eval_Agent__3_.py
```

This script:
- Defines a dataset of test cases in `EXAMPLES`
- Creates or updates a LangSmith dataset called `agent-evals-v1`
- Runs the agent against each test case
- Applies multiple evaluators to score performance
- Reports results in LangSmith

#### Built-in Evaluators

1. **Exact Match Evaluator** – Checks if output exactly matches expected value
2. **LLM Judge Evaluator** – Uses GPT-4o-mini to assess if output is a valid inspirational thought
3. **Smart Router** – Automatically selects the appropriate evaluator based on test case type

#### Editing Test Cases

Modify the `EXAMPLES` list in `eval_Agent__3_.py` to add or change test cases:

```python
EXAMPLES = [
    {
        "input":  {"input": "Your test message here"},
        "output": {"output": "Expected output or <any inspirational thought>"},
    },
    # Add more examples...
]
```

Use `"<any inspirational thought>"` as a sentinel value for flexible matching when exact output is not required.

## Project Structure

```
Simple_Langraph_Agent/
├── dynamic_agent_input.py       # Main agent script (run this for queries)
├── eval_Agent__3_.py            # Evaluation script with LangSmith integration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
└── .env                         # Your API keys (not tracked in git)
```

## How It Works

### Agent Architecture

The agent uses a **ReAct** (Reasoning + Acting) pattern:
- **Input:** User message
- **Reasoning:** LLM decides which tools to invoke
- **Acting:** Tools are called in parallel or sequence as needed
- **Output:** Final response from the agent

### System Prompt

The agent operates under this system prompt:
> "You are a helpful assistant. Make sure that you only respond with whatever is coming as input to the agent, and do not add any extra commentary or explanation."

This ensures clean, focused responses from the agent.

### Available Tools

#### `get_weather(city: str) -> str`
Returns weather information for a given city.
- **Input:** City name (string)
- **Output:** Weather status message
- **Example:** `get_weather("New York")` → `"It's always sunny in New York!"`

#### `create_daily_thought() -> str`
Generates a unique inspirational daily thought using GPT-4o-mini.
- **Input:** None (uses LLM internally)
- **Output:** Short inspirational message (1-2 sentences)
- **Example:** Returns thoughts like "Every day is a new opportunity to grow and learn."

## Configuration

### Model Selection

- **Main Agent:** `gpt-4o` (GPT-4 Omni) – Better reasoning and tool use
- **Daily Thoughts:** `gpt-4o-mini` (GPT-4 Mini) – Cost-effective for text generation
- **Evaluation:** `gpt-4o-mini` – Fast, reliable LLM judge

You can modify these in the respective Python files if needed.

### LangSmith Setup (Optional)

To enable tracing and evaluation:

1. Create a LangSmith account at [smith.langchain.com](https://smith.langchain.com)
2. Generate an API key from your account settings
3. Add the key to your `.env` file
4. Set `LANGSMITH_TRACING=true`
5. Runs will now be logged and visible in the LangSmith dashboard

## Troubleshooting

### "No OPENAI_API_KEY found in environment!"
- Ensure your `.env` file exists and contains `OPENAI_API_KEY`
- Verify the `.env` file is in the same directory as `dynamic_agent_input.py`
- Check that your API key is valid and not expired

### LangSmith tracing not working
- Verify `LANGSMITH_API_KEY` is set in your `.env` file
- Ensure `LANGSMITH_TRACING=true`
- Check that your LangSmith API key is valid
- Note: The agent will still function without LangSmith keys

### Import errors
- Ensure all packages in `requirements.txt` are installed: `pip install -r requirements.txt`
- Try upgrading packages: `pip install --upgrade langchain langchain-openai langgraph`

## Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Core agent/LLM framework |
| `langchain-openai` | OpenAI model integration |
| `langgraph` | Graph-based agent orchestration |
| `python-dotenv` | Environment variable management |
| `requests` | HTTP requests (if needed by tools) |

See `requirements.txt` for pinned versions.

## API Costs

- **Agent queries** use GPT-4o (more expensive, better reasoning)
- **Daily thoughts** use GPT-4o-mini (cheaper)
- **Evaluations** use GPT-4o-mini (cheaper)

Estimated cost per agent query: ~$0.01–$0.05 depending on input/output length.

## Next Steps

- Add more tools (e.g., news, stocks, APIs)
- Extend evaluation test cases
- Integrate with a web framework (Flask, FastAPI)
- Deploy to production with proper error handling
- Monitor costs and performance via LangSmith dashboard

## License

[Add your license here]

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Support

For issues, questions, or suggestions, please open a GitHub issue or contact the maintainers.
