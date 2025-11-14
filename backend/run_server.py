#!/usr/bin/env python
# run_server.py

import sys
import os

# Adicionar backend ao path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
