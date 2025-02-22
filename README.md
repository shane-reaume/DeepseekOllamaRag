# DeepSeek Ollama RAG System

A Retrieval-Augmented Generation (RAG) system using DeepSeek R1 running locally through Ollama, with a Streamlit interface for PDF document Q&A.

## Overview

Original Tutorial: [Setting up Ollama & Running DeepSeek R1 Locally for a Powerful RAG System](https://dev.to/ajmal_hasan/setting-up-ollama-running-deepseek-r1-locally-for-a-powerful-rag-system-4pd4)

This project implements a local RAG system that allows users to:

- Upload PDF documents
- Ask questions about the documents
- Get AI-generated answers using locally running DeepSeek R1 model
- Process documents without sending data to external services

## System Requirements

### Minimum Requirements

- 8GB RAM
- 10GB free disk space
- Python 3.12.3 (tested, other 3.x versions may work)

### Recommended

- 16GB RAM
- NVIDIA GPU with 4GB+ VRAM (for faster processing)
- 20GB free disk space

## Installation Instructions

### 1. Install Ollama

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### macOS

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows

1. Install Windows Subsystem for Linux (WSL2)
2. Follow Linux installation instructions within WSL2
   - Or download from [Ollama Windows](https://ollama.com/download/windows)

### 2. Pull DeepSeek Model

```bash
    ollama pull deepseek-r1:1.5b
```

### 3. Setup Python Environment

#### Create Virtual Environment

Create virtual environment

```bash
python3 -m venv .venv
```

Activate virtual environment

On Linux/MacOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

#### Install Dependencies

Install required packages

```bash
pip install -r requirements.txt
```

### 4. Configure Ollama Settings

The application uses a configuration system to manage Ollama settings:

1. Copy the template configuration:
```bash
cp config.template.py config.py
```

2. Edit `config.py` with your settings:
```python
OLLAMA_CONFIG = {
    "model": "your-preferred-model",
    "base_url": "http://your.ollama.server:11434"
}
```

Note: `config.py` is ignored by git to keep your local settings private.

### 5. PDF Document Management

The application uses two locations for PDF files:

- `/pdf/` directory: Store your permanent PDF collection here
- `temp.pdf`: Working file in root directory (auto-generated when uploading)

When you upload a PDF through the UI:

1. The file is temporarily saved as `temp.pdf` in the root directory
2. This file is processed for the current session
3. The original PDFs in `/pdf/` remain unchanged

Note: Add this to your `.gitignore` to prevent PDFs from being committed:

```bash
*.pdf
```

## Running the Application

1. Ensure Ollama service is running:

    Linux/MacOS

    ```bash
    ollama serve
    ```

    Windows (separate terminal)

    ```bash
    wsl -d Ubuntu -e ollama serve
    ```

2. Start the Streamlit app:

    ```bash
    streamlit run app.py
    ```

3. Open your browser and navigate to:

   - Local URL: http://localhost:8501
   - Network URL: Will be displayed in terminal

## Troubleshooting

### Common Issues

1. **CUDA Errors**
    If you see CUDA initialization errors but have a NVIDIA GPU:

    - Ensure NVIDIA drivers are installed
    - Install CUDA toolkit
    - Set environment variable: export CUDA_VISIBLE_DEVICES=0

2. **Memory Issues**
    If you encounter memory errors:

    - Close other applications
    - Use a smaller model variant
    - Reduce chunk size in the code

3. **Ollama Connection Issues**
    If Ollama fails to connect:

    - Ensure ollama serve is running
    - Check if port 11434 is available
    - Verify firewall settings

### Platform-Specific Notes

#### Linux

- Ensure CUDA drivers are installed for GPU support
- May need to run with sudo for first-time setup

#### MacOS

- M1/M2 chips are supported natively
- Intel Macs may need Rosetta 2

#### Windows

- WSL2 recommended for best performance
- Native Windows support is in beta
- May need to configure Windows Defender exceptions

## References

- [Original Tutorial](https://dev.to/ajmal_hasan/setting-up-ollama-running-deepseek-r1-locally-for-a-powerful-rag-system-4pd4)
- [Ollama Documentation](https://ollama.com/docs)
- [DeepSeek Model Information](https://ollama.com/library/deepseek)
- [Streamlit Documentation](https://docs.streamlit.io)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
