import os
from config import OLLAMA_CONFIG

# Try to import local config, use defaults if not found
try:
    from config import OLLAMA_CONFIG as LOCAL_CONFIG
    OLLAMA_CONFIG.update(LOCAL_CONFIG)
except ImportError:
    pass 