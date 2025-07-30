# IDA HCLI Chat Extension

An extension for ida-hcli to chat with IDA using the MCP server. 

[![PyPI version](https://badge.fury.io/py/ida-hcli.svg)](https://badge.fury.io/py/ida-hcli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Requirements 

### ida-hcli 

You need to have ida-hcli installed. 

See [https://pypi.org/project/ida-hcli/](https://pypi.org/project/ida-hcli/) 

### ida mcp 

The extension works with [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp)

```bash 
pip uninstall ida-pro-mcp
pip install git+https://github.com/mrexodia/ida-pro-mcp
```

## Installation

Add the extension using pipx 

```bash
pipx inject ida-hcli ida-hcli-chat 
```

## Quick Start

```bash
# Login to your Hex-Rays account
hcli chat 
```
