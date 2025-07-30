import os
import sys
from pathlib import Path

TEMPLATES = {
    'agent.py': '''from botnetics import BotneticsApp, Message
import os

app = BotneticsApp(
    api_key=os.getenv("API_KEY", "test-key"),
    gateway_url=os.getenv("GATEWAY_URL", "http://localhost:8000")
)

@app.on_message
def handle_message(message: Message):
    print(f"Received: {message.text} from {message.user_id}")
    return Message(
        text=f"Echo: {message.text}",
        chat_id=message.chat_id,
        user_id=message.user_id
    )

if __name__ == "__main__":
    print("[BOT] Botnetics agent starting...")
    print("[API] Message endpoint: http://localhost:8000/message/")
    app.run()
''',
    'requirements.txt': '''botnetics-agent
python-dotenv
''',
    '.env': '''API_KEY=your_api_key_here
GATEWAY_URL=http://localhost:8000
''',
    'Dockerfile': '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "agent.py"]
''',
    'README.md': '''# My Agent

A simple agent built with Botnetics Agent Framework.

## Setup
1. Edit `.env` with your API key
2. Run: `python agent.py`
3. Test: POST to http://localhost:8000/message/

## Deploy
```bash
docker build -t my-agent .
docker run -p 8000:8000 my-agent
```
'''
}

def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'init':
        print("Usage: botnetics init <project_name>")
        return
    
    project_name = sys.argv[2]
    project_path = Path(project_name)
    
    if project_path.exists():
        print(f"[ERROR] Directory {project_name} already exists!")
        return
    
    project_path.mkdir()
    
    for filename, content in TEMPLATES.items():
        (project_path / filename).write_text(content)
    
    print(f"[SUCCESS] Created {project_name}")
    print(f"[DIR] cd {project_name}")
    print("[CONFIG] Edit .env with your API key")
    print("[RUN] python agent.py")
    print("[API] Test: POST to http://localhost:8000/message/")

if __name__ == "__main__":
    main()
