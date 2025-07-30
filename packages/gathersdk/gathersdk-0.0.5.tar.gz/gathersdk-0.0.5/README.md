# GatherChat Agent SDK

A Python SDK for building intelligent agents that integrate with GatherChat.

## Features

- **Simple API Key Authentication** - No complex OAuth flows, just use your agent key
- **WebSocket-based Communication** - Real-time bidirectional messaging
- **Automatic Reconnection** - Handles network interruptions gracefully
- **Heartbeat Support** - Keeps connections alive with periodic heartbeats
- **Type-Safe Context** - Pydantic models for all data structures
- **Async/Await Support** - Modern Python async patterns
- **Easy to Use** - Get started with just a few lines of code

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/your-org/gatherchat-agent-sdk.git
```

Or for development:

```bash
pip install gathersdk
```

## Quick Start

### 1. Create Your Agent in GatherChat

1. Sign up at GatherChat
2. Go to the Developer Portal  
3. Create a new agent
4. Copy your agent key (shown only once!)

### 2. Write Your Agent

Create `my_agent.py`:

```python
from gatherchat_agent_sdk import MessageRouter

router = MessageRouter()

@router.on_message
async def reply(message: str, user: str) -> str:
    """
    Handle incoming messages.
    
    Args:
        message: The user's message text
        user: The user's display name
    """
    return f"Hello {user}! You said: '{message}'"

if __name__ == "__main__":
    router.run()
```

### 3. Set Up Authentication

Create `.env`:

```env
GATHERCHAT_AGENT_KEY=your-agent-key-here
```

### 4. Run Your Agent

```bash
python my_agent.py
```

That's it! Your agent is now live in GatherChat.

## Agent Context

Every message your agent receives includes rich context:

```python
async def process(self, context: AgentContext) -> str:
    # User information
    user_id = context.user.user_id
    username = context.user.username
    display_name = context.user.display_name
    
    # Chat information
    chat_id = context.chat.chat_id
    chat_name = context.chat.name
    participants = context.chat.participants
    
    # Message information
    prompt = context.prompt  # The user's message
    invocation_id = context.invocation_id  # Unique ID for this invocation
    
    # Conversation history
    for msg in context.conversation_history:
        print(f"{msg.username}: {msg.content}")
    
    # Your response
    return "Your response here"
```

## Advanced Features

### Streaming Responses

For long responses, you can stream chunks:

```python
class StreamingAgent(BaseAgent):
    async def process_streaming(self, context: AgentContext):
        """Stream response chunks."""
        response = "This is a long response..."
        
        # Stream word by word
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.1)  # Simulate processing
```

### Initialization and Cleanup

```python
class StatefulAgent(BaseAgent):
    async def initialize(self):
        """Called once when agent starts."""
        self.db = await connect_to_database()
        self.model = await load_model()
    
    async def cleanup(self):
        """Called when agent shuts down."""
        await self.db.close()
        await self.model.unload()
```

### Custom Validation

```python
class ValidatingAgent(BaseAgent):
    def validate_context(self, context: AgentContext):
        """Validate context before processing."""
        if len(context.prompt) > 1000:
            raise ValueError("Message too long")
        
        if "spam" in context.prompt.lower():
            raise ValueError("Spam detected")
```

### Manual Client Control

For more control, use the `AgentClient` directly:

```python
from gathersdk import AgentClient

async def main():
    agent = MyAgent("my-agent", "Description")
    
    async with AgentClient(agent) as client:
        await client.run()

asyncio.run(main())
```

## Configuration

### Environment Variables

- `GATHERCHAT_AGENT_KEY` - Your agent's API key (required)
- `GATHERCHAT_API_URL` - API base URL (default: `http://localhost:8085`)

### Client Options

```python
from gathersdk import AgentClient

client = AgentClient(
    agent=my_agent,
    agent_key="your-key",  # Override env var
    api_url="https://api.gatherchat.com",  # Override env var
    heartbeat_interval=30  # Seconds between heartbeats
)
```

## Error Handling

The SDK handles errors gracefully:

- **Authentication errors** - Check your agent key
- **Connection errors** - Automatic reconnection with exponential backoff
- **Processing errors** - Errors are logged and reported back to GatherChat
- **Validation errors** - Raised before processing begins

## Examples

See the `examples/` directory for working examples:

- `minimal_agent.py` - The simplest possible agent (perfect starting point)

## Development

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- GitHub Issues: https://github.com/your-org/gatherchat-agent-sdk/issues
- Documentation: https://docs.gatherchat.com/sdk
- Discord: https://discord.gg/gatherchat

## License

MIT License - see LICENSE file for details