# Botnetics Agent

A simple framework for building Telegram agents with Django.

## Installation

```bash
pip install botnetics-agent
```

## Quick Start

```bash
botnetics init my-agent
cd my-agent
python agent.py
```

Test your agent:
```bash
curl -X POST http://localhost:8000/message/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "chat_id": "123", "user_id": "456"}'
```

## Features

- Simple message handling with decorators
- Built-in Django web server
- REST API endpoint for message processing
- Easy project scaffolding
- Docker support

## Usage

Create a new agent:
```python
from botnetics import BotneticsApp, Message

app = BotneticsApp(api_key="your-key")

@app.on_message
def handle_message(message: Message):
    return Message(
        text=f"You said: {message.text}",
        chat_id=message.chat_id,
        user_id=message.user_id
    )

app.run()
```

## License

MIT License
