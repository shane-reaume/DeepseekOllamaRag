# Ollama RAG System

A Retrieval-Augmented Generation (RAG) system using LLM Models running locally through Ollama, with a Streamlit interface for PDF document Q&A.

## Overview

This project implements a local RAG system that allows users to:

- Upload PDF documents
- Ask questions about the documents
- Get AI-generated answers using locally running LLM model
- Process documents without sending data to external services

## Streamlit Interface

The application provides an intuitive web interface with:

### Main Features

- PDF file upload button
- Question input field
- Real-time response display
- Document processing status indicators

### Sidebar Information

- Clear usage instructions
- Current model settings
- Ollama connection status

### Visual Elements

- Progress bars for document processing
- Success/Error notifications
- Formatted response display
- Dark mode support

## Supported Ollama Models

You can use various LLM models with this application. Here are some recommended options:

### General Purpose Models

- Mistral (7B): `mistral` - Good balance of performance and speed
- Llama2 (70B): `llama2` - Meta's latest model
- Gemma (7B): `gemma` - Google's efficient model
- Qwen (72B): `qwen` - Alibaba's multilingual model

### Specialized Models

- DeepSeek Coder: `deepseek-coder` - Optimized for code
- CodeLlama: `codellama` - Specialized for programming tasks
- Phi-3: `phi` - Microsoft's compact but capable model

### Large Models

- Mixtral (8x7B): `mixtral` - Powerful mixture-of-experts model
- Dolphin Mixtral: `dolphin-mixtral` - Enhanced Mixtral variant
- DeepSeek (67B): `deepseek` - High-performance model

To use a specific model:

1. Pull the model:

```bash
ollama pull model-name
```

1. Update your config.py:

```python
OLLAMA_CONFIG = {
    "model": "model-name",
    "base_url": "your-ollama-server"
}
```

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

Choose one of these three setup methods:

### Method 1: Using External Ollama Server

If you have Ollama running on another machine (e.g., http://142.134.0.99:11434):

1. Clone the repository

```bash
git clone https://github.com/shane-reaume/DeepseekOllamaRag.git
cd DeepseekOllamaRag
```

1. Run with Docker (recommended):

```bash
# Edit docker-compose.yml to point to your Ollama server
docker-compose up --build
```

Or run locally:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
# Edit config.py with your Ollama server address
streamlit run app.py
```

### Method 2: Local Setup (No Docker)

Run everything locally on your machine:

1. Install Ollama for your platform:
   - Linux/MacOS: `curl -fsSL https://ollama.com/install.sh | sh`
   - Windows: Download from [Ollama Windows](https://ollama.com/download/windows)

2. Start Ollama:

```bash
ollama serve
```

3. Pull the model:

```bash
ollama pull deepseek-r1:1.5b
```

4. Setup Python and run:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
streamlit run app.py
```

### Method 3: Full Docker Setup

Run both Ollama and the app in Docker:

1. Use the local Docker compose file:

```bash
docker-compose -f docker-compose.local.yml up --build
```

2. Pull the model (in a new terminal):

```bash
docker exec deepseekollama_ollama_1 ollama pull deepseek-r1:1.5b
```

### Platform-Specific Notes

#### Linux

- Native Docker support
- GPU acceleration available with NVIDIA drivers
- May need sudo for Ollama installation

#### macOS

- Native support for M1/M2 chips
- Intel Macs may need Rosetta 2
- Docker Desktop recommended

#### Windows

- WSL2 recommended for best performance
- Run Ollama through WSL2 or use native Windows installer
- Docker Desktop required

## PDF Document Management

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

## Docker Installation

### Using Docker Compose (Recommended)

1. Build and start the services:
```bash
docker-compose up --build
```

2. Pull the DeepSeek model (in a separate terminal):
```bash
docker exec deepseekollama_ollama_1 ollama pull deepseek-r1:1.5b
```

3. Access the application at:
   - http://localhost:8501

### Manual Docker Setup

1. Build the application image:
```bash
docker build -t ollama-rag .
```

2. Run Ollama container:
```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
```

3. Pull your preferred model:
```bash
docker exec ollama ollama pull mistral
```

4. Run the application container:
```bash
docker run -d --name ollama-rag \
  -p 8501:8501 \
  --link ollama \
  -e OLLAMA_HOST=http://ollama:11434 \
  ollama-rag
```

### Docker Volumes

The application uses two Docker volumes:
- `ollama_data`: Persists Ollama models and data
- `./pdf:/app/pdf`: Mounts local PDF directory to container

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
- [Model Information](https://ollama.com/library)
- [Streamlit Documentation](https://docs.streamlit.io)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
