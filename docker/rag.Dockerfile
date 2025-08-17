# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Project root requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the RAG module code
COPY src/rag /app/src/rag
COPY data/chroma_db /app/data/chroma_db



# Application execution command (FastAPI app)
CMD ["python", "src/rag/rag_service.py", "--mode", "api"]