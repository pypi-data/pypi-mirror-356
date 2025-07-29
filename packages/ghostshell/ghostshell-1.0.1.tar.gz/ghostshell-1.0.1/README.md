
# ghostshell

A Netcat-style remote command execution tool using raw Python sockets.

## Features

- Raw socket client/server
- CLI and importable API
- Supports multiple requests per session

## Installation 
### From PIP
```bash
pip install ghostshell
```

### Manual Installation using setup.py
- Clone this git repo
- cd `ghostshell`
- Run
```bash
pip install .
```

## CLI Usage

### For Code/module CLI:
```bash
 python -m ghostshell.cli.main serve --host 0.0.0.0 --port 9999
 python -m ghostshell.cli.main connect --host 127.0.0.1 --port 9999
```

### For Installed CLI package:
```bash
ghostshell serve --host 0.0.0.0 --port 9999
ghostshell connect --host 127.0.0.1 --port 9999
```

## Python Usage

```python
from ghostshell.core.server import RemoteServer
from ghostshell.core.client import RemoteClient

server = RemoteServer("0.0.0.0", 9999)
server.start()

client = RemoteClient("127.0.0.1", 9999)
client.connect()

print(client.send_command("whoami"))
client.close()
```

## License

MIT
