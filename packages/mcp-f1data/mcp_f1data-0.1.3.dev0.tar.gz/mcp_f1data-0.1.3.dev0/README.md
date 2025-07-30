# 🏎️ MCP Server F1Data

<img src="./content/example.gif" width="1000">

A Model Context Protocol (MCP) server for interacting with F1Data through LLM interfaces like Claude. **You will need to have Claude installed on your system to continue.**

## Getting Started
First of all, you need to install `mcp-f1data` package from pypi with pip, using the following command:
```commandline
pip install mcp-f1data
```

To use `mcp-f1data` server in claude can be configured by adding the following to your configuration file.
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the F1Data MCP server configuration:
```json
{
  "mcpServers": {
    "mcp-f1data": {
        "command": "python",
        "args": [ "-m", "mcp-f1data" ]
    }
  }
}
```

## Tools 
- `fastest lap`
- `lap`
- `top speed`
- `total laps`
- `driver team`
- `team driver`
- `box laps`
- `deleted laps`

## Instalation
Active the virtual environment and install the requirements using:
```commandline
.\.venv\Scripts\activate
```

Install the mcp server in Claude using the following command:
```commandline
mcp install .\server.py
```

## Requirements
The requirementes used to build this MCP server are:
- `fastf1`
- `pandas`
- `fastmcp`
- `websockets`
- `mcp`
- `pydantic`

## Testing 
You can test the server using the MCP Inspector:
```commandline
mcp dev .\server.py
```

## License
This project is licensed under the MIT <a href="https://github.com/Maxbleu/mcp-f1data/blob/master/LICENSE">LICENSE</a> - see the details.
