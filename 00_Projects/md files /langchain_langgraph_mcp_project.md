# 🧠 LangChain + LangGraph + MCP Mastery Project: ResearchMind

> **Mentor note:** You've watched the videos. You know the concepts exist. What you don't have yet is the *muscle memory* — the ability to stare at a blank file and know what to reach for. That's what this 15 days builds. Expect to feel stuck. That's the signal you're learning, not failing.

**Duration:** 15 days · ~2 hrs/day  
**Stack:** LangChain · LangGraph · MCP · FastAPI · JWT Auth · SQLite  
**Model:** Gemini 2.0 Flash (via `langchain_google_genai`) or any OpenAI-compatible model

---

## 🎯 What You're Building

**ResearchMind** — an AI research assistant API where users can:

- Submit a research topic and get a multi-step AI-generated research report
- The agent autonomously decides what to search, what to read, how to structure findings
- Conversations are stateful — the agent remembers previous turns per session
- MCP tools (web search, file reading) are plugged in as agent tools
- Everything is behind JWT auth — each user has isolated research sessions
- Sessions and reports are persisted to a database

This is not a chatbot wrapper. It's an **agentic pipeline** with real tool use, state management, and a production-grade API layer on top.

---

## 📌 Before You Start — Required Reading

Do this before Day 1. Not optional.

1. **LangChain Expression Language (LCEL)** — `|` operator, `RunnableSequence`, `RunnableParallel`, `RunnablePassthrough`. Read the official LCEL conceptual doc, not a tutorial.
2. **LangGraph conceptual overview** — nodes, edges, state, `StateGraph`. Read: https://langchain-ai.github.io/langgraph/concepts/
3. **MCP spec (5 min read)** — what a tool server is, how clients call tools. Read: https://modelcontextprotocol.io/introduction
4. **`langchain_google_genai` quickstart** — know how to instantiate `ChatGoogleGenerativeAI` and call `.invoke()` before Day 1.

> **Mentor note:** The biggest mistake after watching videos is jumping straight to building complex graphs. The videos made it look easy because someone already knew what they were doing. Your job this week is to *slow down* and understand why each abstraction exists before stacking them.

---

## 🗓️ Phase 1 (Days 1–4) — LangChain Core, Properly

The goal of this phase is not to build features. It's to understand the abstractions so deeply that you could explain them to someone else.

---

### Day 1 — LCEL and the Runnable Protocol

**What to build:** A chain that takes a research topic, generates 5 sub-questions to investigate, and formats them as structured output.

**Core concepts:**
- The `Runnable` protocol — `.invoke()`, `.stream()`, `.batch()`, `.ainvoke()` — every component in LangChain implements this
- `ChatPromptTemplate` with `MessagesPlaceholder` — why templates exist instead of raw f-strings
- `StrOutputParser` vs `PydanticOutputParser` vs `with_structured_output()` — know *when* to use each
- `RunnablePassthrough` — passing input through unchanged while a parallel branch processes it
- `RunnableParallel` — running multiple chains on the same input simultaneously

**What to implement:**
```python
# Chain 1: Topic → Sub-questions (structured output)
class ResearchPlan(BaseModel):
    topic: str
    sub_questions: list[str]
    estimated_complexity: Literal["simple", "moderate", "complex"]

# Use with_structured_output() here — it's the cleanest approach for Pydantic models
plan_chain = prompt | llm.with_structured_output(ResearchPlan)

# Chain 2: Topic → Research plan summary (string output)
# Use RunnableParallel to run both chains on the same topic input
```

**Where to learn:**
- https://python.langchain.com/docs/concepts/lcel/
- https://python.langchain.com/docs/concepts/runnables/

> **Keynote:** `with_structured_output()` is almost always better than `PydanticOutputParser` for modern models. `PydanticOutputParser` works by injecting format instructions into the prompt and parsing the text response — fragile. `with_structured_output()` uses the model's native tool/function calling — reliable. Know both exist, use the latter.

---

### Day 2 — Memory and Message History

**What to build:** A conversational research assistant that remembers what topics were discussed in a session.

**Core concepts:**
- `BaseChatMessageHistory` — the interface for storing messages
- `InMemoryChatMessageHistory` — for understanding the concept
- `RunnableWithMessageHistory` — wraps any chain to add history management
- `get_session_history` callable — how LangChain retrieves history per session ID
- `MessagesPlaceholder` — where history gets injected in your prompt
- The difference between `HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage`

**What to implement:**
```python
# A chain that:
# 1. Accepts a session_id and user message
# 2. Loads that session's message history
# 3. Generates a response aware of previous turns
# 4. Saves the exchange to history

chain_with_history = RunnableWithMessageHistory(
    your_chain,
    get_session_history,  # callable: session_id -> ChatMessageHistory
    input_messages_key="input",
    history_messages_key="chat_history",
)
```

**Where to learn:**
- https://python.langchain.com/docs/concepts/chat_history/
- https://python.langchain.com/docs/how_to/message_history/

> **Keynote:** `RunnableWithMessageHistory` is the LangChain way. LangGraph has its own, more powerful approach to memory (you'll use that in Week 2). For simple conversational chains, `RunnableWithMessageHistory` is fine. For complex agents with branching and tool use, LangGraph's checkpointing is the right tool. Understanding *why* LangGraph replaced this for complex cases is an important conceptual gap to close by Day 7.

---

### Day 3 — Tools and Tool Calling

**What to build:** Give your chain tools — web search and a simple calculator — and watch the model decide when to use them.

**Core concepts:**
- `@tool` decorator — the simplest way to define a LangChain tool
- `StructuredTool.from_function()` — when you need more control
- Tool schema — how LangChain serializes your function signature into a JSON schema the model understands
- `bind_tools()` — attaching tools to an LLM
- `AIMessage.tool_calls` — reading what the model *wants* to call
- `ToolMessage` — the result you feed back after calling the tool
- `tool_choice="auto"` vs `"required"` vs specific tool name

**What to implement:**
```python
@tool
def search_web(query: str) -> str:
    """Search the web for information about a topic. Use this when you need current information."""
    # Use DuckDuckGo or Tavily — Tavily has a free tier and LangChain integration
    ...

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Input must be a valid Python expression."""
    ...

# Bind tools to LLM — model will output tool_calls when it wants to use them
llm_with_tools = llm.bind_tools([search_web, calculate])

# Manually execute the tool call loop once (you'll automate this in LangGraph)
response = llm_with_tools.invoke(messages)
if response.tool_calls:
    # execute each tool call, build ToolMessages, pass back to model
    ...
```

**Where to learn:**
- https://python.langchain.com/docs/concepts/tools/
- https://python.langchain.com/docs/how_to/tool_calling/

> **Keynote:** Do the tool call loop *manually* today — don't use an agent or LangGraph yet. The point is to understand what's actually happening: model says "call X with Y", you call X, get result, pass result back, model continues. LangGraph automates this loop. You should understand what it's automating before you use it.

---

### Day 4 — Retrieval and RAG (Focused)

**What to build:** A document Q&A chain — user uploads text, the system can answer questions about it.

**Core concepts:**
- `RecursiveCharacterTextSplitter` — why chunking exists, how `chunk_size` and `chunk_overlap` affect retrieval
- `Chroma` (in-memory, no server needed) — embedding store for this project
- `GoogleGenerativeAIEmbeddings` — your embedding model
- `VectorStoreRetriever` — `.as_retriever()`, `search_type`, `k`
- `create_retrieval_chain` — the standard RAG chain builder
- `create_stuff_documents_chain` — combines retrieved docs into prompt context
- `RunnablePassthrough` for passing `source_documents` alongside the answer

**What to implement:**
```python
# The retrieval chain that ResearchMind will use internally:
# user question → retrieve relevant chunks → stuff into context → generate answer with sources

retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 20})
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
```

**Where to learn:**
- https://python.langchain.com/docs/concepts/rag/
- https://python.langchain.com/docs/how_to/qa_chat_history_how_to/

> **Keynote:** MMR (Maximal Marginal Relevance) retrieval is almost always better than plain similarity for real use cases. Similarity search returns the top-k most similar chunks, which often means 5 chunks saying the same thing. MMR balances relevance *and* diversity — it picks chunks that are relevant but not redundant. Use `search_type="mmr"` by default.

---

## 🗓️ Phase 2 (Days 5–9) — LangGraph: Stateful Agents

> **Mentor note:** This is where the project gets real. LangGraph is not "LangChain but more complex". It's a fundamentally different mental model: you're defining a *state machine* where nodes are computation steps and edges are transitions. The hardest part for most people is thinking in state machines instead of sequential code. Take your time on Days 5 and 6.

---

### Day 5 — LangGraph Fundamentals: State and Nodes

**What to build:** A minimal research graph — 3 nodes, 1 conditional edge.

**Core concepts:**
- `TypedDict` as graph state — why LangGraph uses TypedDict, how `Annotated[list, operator.add]` works for append-only fields
- `StateGraph` — the graph builder
- Nodes as functions — `(state: State) -> dict` — why nodes return *partial* state updates
- `add_node()`, `add_edge()`, `set_entry_point()`, `set_finish_point()`
- `compile()` — what it does, what `checkpointer` means
- `END` — the terminal node
- Conditional edges — `add_conditional_edges(node, routing_function, {output: next_node})`

**What to build:**
```python
class ResearchState(TypedDict):
    topic: str
    sub_questions: Annotated[list[str], operator.add]  # accumulates across nodes
    research_notes: Annotated[list[str], operator.add]
    final_report: str
    messages: Annotated[list[BaseMessage], operator.add]

# Graph: plan_research → should_continue (conditional) → research_topic OR generate_report
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/concepts/low_level/
- https://langchain-ai.github.io/langgraph/tutorials/introduction/

> **Keynote:** The single most common LangGraph mistake: returning the full state from a node instead of just the fields you're updating. Nodes should return `{"field_name": new_value}` — only what changed. LangGraph merges this with the existing state. If you return the full state, you'll get confusing bugs especially with `Annotated` reducers.

---

### Day 6 — The ReAct Agent Pattern

**What to build:** A ReAct (Reason + Act) agent graph — the canonical agentic pattern.

**Core concepts:**
- ReAct loop: `think → act → observe → think → ...`
- `ToolNode` — LangGraph's built-in node that executes tool calls from `AIMessage.tool_calls`
- `tools_condition` — built-in conditional edge that routes to `ToolNode` if model called a tool, else `END`
- Why ReAct agents can loop — and how to add `recursion_limit` to prevent infinite loops
- `HumanMessage`, `AIMessage`, `ToolMessage` flow in the messages state

**What to build:**
```python
# The core ResearchMind agent graph:
# agent (LLM with tools) → tools_condition → ToolNode → back to agent
#                                          ↘ END (when no more tool calls)

graph = StateGraph(ResearchState)
graph.add_node("agent", call_model)       # LLM with tools bound
graph.add_node("tools", ToolNode(tools))  # executes tool calls

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")          # always go back to agent after tool use
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/tutorials/introduction/
- https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/

> **Keynote:** `ToolNode` is magic — it reads `AIMessage.tool_calls` from the state, executes each tool, wraps results in `ToolMessage`, and appends them to state. You don't need to write the tool execution loop manually (which you did on Day 3 — now you appreciate why `ToolNode` exists). But you should know what it's doing internally, because when tools fail, you need to debug at that level.

---

### Day 7 — Checkpointing and Persistent State

**What to build:** Add persistence to your graph — sessions survive server restarts.

**Core concepts:**
- Why in-memory state is useless for production (server restart = everything gone)
- `SqliteSaver` — the simplest persistent checkpointer
- `PostgresSaver` — for production (just know it exists)
- `thread_id` — how LangGraph identifies sessions
- `config = {"configurable": {"thread_id": "user-123-session-456"}}`
- `graph.get_state(config)` — inspecting current state of a thread
- `graph.update_state(config, values)` — manually patching state (powerful for human-in-the-loop)
- `interrupt_before` — pausing graph execution for human review

**What to implement:**
```python
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async with AsyncSqliteSaver.from_conn_string("research_sessions.db") as checkpointer:
    graph = compile_graph(checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": session_id}}
    
    # First invocation — starts fresh
    result = await graph.ainvoke({"topic": "quantum computing"}, config=config)
    
    # Second invocation — continues from where it left off
    result = await graph.ainvoke({"input": "focus on error correction"}, config=config)
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/concepts/persistence/
- https://langchain-ai.github.io/langgraph/how-tos/persistence/

> **Keynote:** `thread_id` is the most important concept in LangGraph for production. It's how you isolate state per user per conversation. In ResearchMind, your `thread_id` will be `{user_id}:{session_id}`. Never let two users share a thread_id. When you integrate with FastAPI on Day 10, this is what ties the auth layer to the agent layer.

---

### Day 8 — Multi-Node Research Pipeline

**What to build:** Upgrade the basic ReAct loop into a multi-stage research pipeline with specialized nodes.

**Core concepts:**
- Multiple specialized nodes vs one general agent — tradeoffs
- `Send` API — dynamic parallel edges (fan-out): run the same node for each item in a list
- `operator.add` reducers collecting results from parallel branches
- Subgraphs — a graph as a node inside another graph
- Node retries — `node.retry_policy`

**What to build:**

```
[plan_research] → [Send: research_question × N] → [synthesize_findings] → [write_report]
     ↑ generates N sub-questions      ↑ runs in parallel           ↑ combines all notes
```

```python
from langgraph.types import Send

def plan_research(state: ResearchState):
    # Generate sub-questions
    plan = plan_chain.invoke({"topic": state["topic"]})
    # Fan out: one research task per sub-question
    return [Send("research_question", {"question": q}) for q in plan.sub_questions]
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/how-tos/map-reduce/
- https://langchain-ai.github.io/langgraph/concepts/low_level/#send

> **Keynote:** The `Send` API (map-reduce pattern) is one of LangGraph's most powerful features and is almost never covered in beginner tutorials. It lets you spawn N parallel branches dynamically at runtime — the number of branches isn't known until execution. This is how you'd parallelize research across multiple sub-questions instead of doing them sequentially, cutting your research time significantly.

---

### Day 9 — Human-in-the-Loop and Streaming

**What to build:** Add the ability to pause before writing the final report, let the user review and approve, then continue.

**Core concepts:**
- `interrupt_before=["write_report"]` — pause before a specific node
- `graph.get_state()` — reading what state the graph paused in
- `graph.update_state()` — injecting human feedback into state
- Resuming with `None` input — `graph.ainvoke(None, config=config)`
- Streaming: `graph.astream()` vs `graph.astream_events()`
- `astream_events` event types: `on_chain_start`, `on_llm_stream`, `on_tool_end`
- Streaming tokens to the API response: `StreamingResponse` in FastAPI

**What to implement:**
```python
# Pause before writing the report
graph = graph_builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["write_report"]
)

# API endpoint: GET /sessions/{id}/state → returns current state for user to review
# API endpoint: POST /sessions/{id}/approve → calls update_state then resumes
# API endpoint: POST /sessions/{id}/stream → streams tokens via SSE
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
- https://langchain-ai.github.io/langgraph/how-tos/streaming/

> **Keynote:** Streaming is not optional for production AI APIs. Users will not wait 30 seconds staring at a blank screen while the model generates a research report. `astream_events` is the right API — it gives you fine-grained control over *which* events to stream (you might only want to stream the final report generation, not internal tool calls). FastAPI's `StreamingResponse` with `text/event-stream` content type is the SSE implementation.

---

## 🗓️ Phase 3 (Days 10–12) — FastAPI Integration + Auth

---

### Day 10 — FastAPI Layer + Session Management

**What to build:** Wrap the LangGraph agent in a FastAPI application with full session management.

**Core concepts:**
- Graph as a singleton — compile once at startup, reuse across requests
- `lifespan` context manager — initialize graph, DB, checkpointer at startup
- Dependency injection tying auth → session ownership
- Async graph invocation inside async route handlers
- Session model in SQLAlchemy — `user_id`, `session_id`, `topic`, `status`, `created_at`

**What to build:**
```
routers/
├── sessions.py    # POST /sessions, GET /sessions, GET /sessions/{id}
├── research.py    # POST /sessions/{id}/run, POST /sessions/{id}/approve
├── stream.py      # GET /sessions/{id}/stream (SSE)
└── auth.py        # Same JWT auth from BookVault

graph.py           # Graph compilation, tool setup — imported once in main.py
```

**The key pattern:**
```python
# In main.py lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string("sessions.db") as checkpointer:
        app.state.graph = compile_research_graph(checkpointer)
        app.state.checkpointer = checkpointer
        yield

# In dependency
def get_graph(request: Request) -> CompiledGraph:
    return request.app.state.graph
```

> **Keynote:** The graph **must** be compiled once and reused — not compiled per request. Compilation is expensive and the checkpointer connection would be lost if you recreated it every request. `app.state` is FastAPI/Starlette's mechanism for storing application-level state. This is also where you'd store a Redis connection, a DB connection pool, etc.

---

### Day 11 — Auth Integration + Session Isolation

**What to build:** Wire JWT auth from Phase 3 of BookVault into ResearchMind. Ensure users can only access their own sessions.

**Core concepts:**
- Re-using the JWT auth dependency pattern you already built
- Ownership check — `session.user_id == current_user.id` before every operation
- `thread_id` namespacing — `f"{user_id}:{session_id}"` for LangGraph checkpointer
- 403 vs 404 — don't leak whether a resource exists to unauthorized users

**What to implement:**
```python
async def get_user_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResearchSession:
    session = await db.get(ResearchSession, session_id)
    if not session:
        raise HTTPException(404)
    if session.user_id != current_user.id:
        raise HTTPException(403)  # NOT 404 — user knows they're unauthorized, not that it doesn't exist
    return session
```

> **Keynote:** The 403 vs 404 decision is not just politeness — it's a security decision. Returning 404 for unauthorized resources prevents enumeration attacks (attacker can't discover what resource IDs exist). Returning 403 is appropriate when the user *already knows* the resource exists (e.g., they created it). Know the tradeoff and pick deliberately.

---

### Day 12 — Streaming Responses (SSE)

**What to build:** Stream research report generation token-by-token to the client.

**Core concepts:**
- `StreamingResponse` with `text/event-stream` media type
- Server-Sent Events (SSE) format: `data: {json}\n\n`
- `graph.astream_events()` — filtering to relevant events only
- Handling SSE in clients (brief — you're not building a frontend, just understand the protocol)
- Backpressure — what happens when the client reads slower than you write

**What to implement:**
```python
@router.get("/sessions/{session_id}/stream")
async def stream_research(
    session_id: str,
    session: ResearchSession = Depends(get_user_session),
    graph: CompiledGraph = Depends(get_graph),
):
    async def event_generator():
        config = {"configurable": {"thread_id": f"{session.user_id}:{session_id}"}}
        async for event in graph.astream_events(None, config=config, version="v2"):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            elif event["event"] == "on_chain_end" and event["name"] == "write_report":
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

> **Keynote:** SSE is strictly one-directional (server → client) and doesn't require WebSockets. For AI token streaming, SSE is almost always the right choice over WebSockets — simpler, HTTP/2 compatible, automatic reconnection in browsers. Use WebSockets only when you need bidirectional real-time communication. Most AI chatbots you've used (ChatGPT, Claude) use SSE for token streaming, not WebSockets.

---

## 🗓️ Phase 4 (Days 13–15) — MCP Integration + Polish

---

### Day 13 — MCP: What It Is and How to Use It

**What to build:** Connect your agent to real MCP tool servers.

**Core concepts:**
- MCP architecture: host ↔ client ↔ server. Your FastAPI app is the host. LangChain's MCP client talks to the server.
- MCP transport types: `stdio` (local process) vs `sse` (remote HTTP server)
- `langchain_mcp_adapters` — converts MCP tool schemas into LangChain `Tool` objects
- Tool discovery — MCP servers advertise their available tools
- `MultiServerMCPClient` — connecting to multiple MCP servers simultaneously

**What to implement:**
```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient({
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/research"],
        "transport": "stdio",
    },
    "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {"BRAVE_API_KEY": settings.brave_api_key},
        "transport": "stdio",
    },
}) as client:
    tools = await client.get_tools()
    # These are now regular LangChain Tool objects — bind to LLM as normal
    llm_with_tools = llm.bind_tools(tools)
```

**MCP servers to use:**
- `@modelcontextprotocol/server-filesystem` — read/write files (save research to disk)
- `@modelcontextprotocol/server-brave-search` — real web search (Brave has free API tier)
- Or `@modelcontextprotocol/server-fetch` — fetch and parse web pages

**Where to learn:**
- https://modelcontextprotocol.io/introduction
- https://github.com/langchain-ai/langchain-mcp-adapters
- MCP server list: https://github.com/modelcontextprotocol/servers

> **Keynote:** MCP is the USB-C of AI tools. Before MCP, every AI framework had its own tool format — LangChain tools don't work in LlamaIndex, CrewAI tools don't work in LangGraph, etc. MCP standardizes the tool interface so a tool server built for one framework works in all. This is why it matters strategically — not just as a feature to implement, but as an industry direction. Anthropic created MCP, which is why you'll see it everywhere in the Claude/Anthropic ecosystem.

---

### Day 14 — MCP in the Agent Graph + Tool Lifecycle

**What to build:** Replace your hand-coded tools with MCP tools, manage the client lifecycle properly.

**Core concepts:**
- MCP client lifecycle — must stay open for the duration of tool availability
- Passing tools into the graph at compile time vs runtime
- `ToolNode` with dynamically loaded MCP tools
- Tool error handling — what happens when an MCP tool server crashes
- Saving research output to filesystem via MCP (write tool results to a file)

**Architecture shift:**
```python
# main.py lifespan — MCP client lives as long as the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string(...) as checkpointer:
        async with MultiServerMCPClient({...}) as mcp_client:
            tools = await mcp_client.get_tools()
            app.state.graph = compile_research_graph(checkpointer, tools)
            app.state.mcp_client = mcp_client
            yield
```

**What to notice:** The MCP client must live inside the `lifespan` context. If you close it, tools stop working. If you recreate it per request, you pay the startup cost every time and the connection to the tool server is unstable. Lifetime management is the hardest part of MCP in production.

> **Keynote:** One thing that trips up almost everyone: MCP tools have async setup. The `async with MultiServerMCPClient(...)` block starts the tool server processes (or connects to remote servers) and keeps them alive. In a FastAPI app, this means the lifespan is the right place. Outside of a web app (e.g., scripts), you'd wrap your entire main() in this context. Letting the context close early means tool calls will fail silently or with confusing errors.

---

### Day 15 — Polish, Testing, and What Comes Next

**What to build:** Clean the codebase up and write meaningful tests for the agent pipeline.

**Testing an agent — what's different:**
- Unit testing individual nodes — much easier than testing the full graph
- Mocking LLM calls — `langchain_core.language_models.fake.FakeListChatModel`
- Mocking tool calls — override tools with fake implementations
- Testing graph structure — `graph.get_graph().nodes`, `.edges`
- Integration test: run full graph with real LLM on a simple topic, assert structure of output

**What to write:**
```python
# Test individual nodes with fake LLM
def test_plan_research_node():
    fake_llm = FakeListChatModel(responses=[json.dumps({
        "topic": "quantum computing",
        "sub_questions": ["What is superposition?", "What is entanglement?"],
        "estimated_complexity": "moderate"
    })])
    state = {"topic": "quantum computing", "messages": [], ...}
    result = plan_research_node(state)  # call node function directly
    assert len(result["sub_questions"]) == 2

# Test full graph with interrupt
async def test_human_in_the_loop():
    graph = compile_graph(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "test-1"}}
    
    # Run until interrupt
    result = await graph.ainvoke({"topic": "AI safety"}, config=config)
    
    # Should be paused before write_report
    state = graph.get_state(config)
    assert state.next == ("write_report",)
    
    # Resume
    await graph.ainvoke(None, config=config)
```

**Where to learn:**
- https://langchain-ai.github.io/langgraph/how-tos/testing/
- LangChain's `FakeListChatModel` for deterministic testing

> **Mentor note:** Testing agents is genuinely hard, and most engineers skip it or do it badly. The discipline is: test nodes as pure functions, test the graph structure, and keep full end-to-end tests to a minimum (expensive and flaky). By the end of today, you should have node-level tests for at least 3 nodes and one integration test that runs the full happy path.

---

## 📂 Final Project Structure

```
researchmind/
├── core/
│   ├── config.py          # pydantic-settings
│   ├── exceptions.py
│   └── security.py        # JWT utilities (reused from BookVault)
├── graph/
│   ├── state.py           # ResearchState TypedDict
│   ├── nodes.py           # All node functions
│   ├── edges.py           # Routing logic, conditions
│   ├── tools.py           # @tool definitions (non-MCP tools)
│   └── builder.py         # compile_research_graph()
├── mcp/
│   └── client.py          # MCP server config, client setup
├── models/
│   ├── user.py
│   └── session.py         # ResearchSession SQLAlchemy model
├── repositories/
│   └── session.py
├── routers/
│   ├── auth.py
│   ├── sessions.py
│   ├── research.py
│   └── stream.py
├── schemas/
│   ├── session.py
│   ├── research.py        # ResearchPlan, ResearchReport Pydantic models
│   └── errors.py
├── dependencies/
│   └── auth.py
├── tests/
│   ├── conftest.py
│   ├── test_nodes.py
│   ├── test_graph.py
│   └── test_api.py
├── database.py
├── main.py
├── .env.example
└── pyproject.toml
```

---

## 🗺️ Concept Map

```
User Request
     │
     ▼
FastAPI (JWT Auth) ─── validates token ──► reject 401
     │
     ▼
Session lookup ──── not owned by user ──► reject 403
     │
     ▼
LangGraph Graph (thread_id = user_id:session_id)
     │
     ├─► [plan_research node]
     │        │ generates sub-questions
     │        ▼
     ├─► [Send → research_question × N] (parallel)
     │        │ each branch: ReAct agent with MCP tools
     │        ▼
     ├─► [synthesize_findings node]
     │        │ combines notes from all branches
     │        ▼
     ├─► [INTERRUPT] ◄── human reviews, optionally edits state
     │        │
     ├─► [write_report node]
     │        │ streams tokens via SSE
     │        ▼
     └─► [save_to_filesystem via MCP tool]
```

---

## 🔑 Core Concepts Summary Table

| Day | What You Learn | Why It Matters |
|-----|---------------|----------------|
| 1 | LCEL, Runnable protocol | Everything in LangChain is a Runnable. This is the foundation. |
| 2 | Message history, `RunnableWithMessageHistory` | Stateless LLMs need external memory |
| 3 | Tool definition, tool calling loop (manual) | Understand what agents automate |
| 4 | RAG, retrieval chain, MMR | Core pattern for knowledge-grounded responses |
| 5 | StateGraph, TypedDict state, reducers | LangGraph's core abstraction |
| 6 | ReAct loop, `ToolNode`, `tools_condition` | The canonical agentic pattern |
| 7 | Checkpointing, `thread_id`, persistence | Production requirement — memory that survives restarts |
| 8 | `Send` API, parallel fan-out, subgraphs | Parallelism and modular graph design |
| 9 | Interrupts, `astream_events`, SSE | Human-in-the-loop and streaming for real UX |
| 10 | FastAPI + graph lifecycle, `app.state` | Wiring agents into a real API |
| 11 | Auth + session isolation, 403 vs 404 | Multi-user security model |
| 12 | `StreamingResponse`, SSE format | Token streaming end-to-end |
| 13 | MCP concepts, `MultiServerMCPClient`, tool discovery | The new standard for AI tool interop |
| 14 | MCP lifecycle, tool server management | Production MCP patterns |
| 15 | Node-level testing, `FakeListChatModel`, integration tests | Testing agents without losing your mind |

---

## 📦 Dependencies

```toml
[project]
name = "researchmind"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.115",
    "langchain>=0.3",
    "langchain-google-genai>=2.0",
    "langgraph>=0.2",
    "langgraph-checkpoint-sqlite",
    "langchain-mcp-adapters",
    "langchain-chroma",
    "sqlalchemy[asyncio]>=2.0",
    "aiosqlite",
    "pydantic>=2.0",
    "pydantic-settings",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-multipart",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    "httpx",
]
```

> You'll need Node.js installed for MCP server processes (`npx` commands).

---

## 🧠 What You Should Be Able to Explain at the End

- Why `Annotated[list[str], operator.add]` in TypedDict state and what happens without the reducer
- The difference between `graph.invoke()` and `graph.stream()` and `graph.astream_events()`
- Why the MCP client lives in `lifespan` and what breaks if it doesn't
- How `thread_id` namespacing prevents one user from seeing another's state
- What `interrupt_before` does at the checkpointer level — not just "it pauses"
- The difference between a LangGraph subgraph and a node that calls another chain
- Why SSE is better than WebSockets for token streaming

---

## 🔭 What's Next (After This Project)

These are the natural follow-ups — you'll be ready for them after this:

- **LangGraph Studio** — visual graph debugging (massive productivity tool)
- **LangSmith** — tracing, eval, prompt management in production
- **Long-term memory** — `langgraph-checkpoint-postgres` + semantic search over past sessions
- **Multi-agent architectures** — supervisor agent delegating to specialist sub-agents
- **RAGAS** — evaluating RAG quality programmatically
- **LangGraph Platform** — deploying graphs as managed services (relevant for FAANG interviews)
