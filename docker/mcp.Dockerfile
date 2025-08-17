# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Project root requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP module code
COPY src/mcp /app/src/mcp

# Application execution command (FastAPI app)
CMD ["uvicorn", "src.mcp.mcp_agent:app", "--host", "0.0.0.0", "--port", "8000"]
