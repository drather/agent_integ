# Agent Integration Project Setup Guide

이 문서는 `agent_integ` 프로젝트의 개발 환경 설정 및 서비스 실행 방법을 안내합니다. `mcp`와 `rag` 서비스는 로컬 Python 프로세스로 실행되며, `virtual_system` (WAS, Web)은 Docker 컨테이너로 실행됩니다.

## 1. 초기 설정 (최초 1회만 수행)

1.  **프로젝트 루트로 이동:**
    ```bash
    cd D:\workspace\agent_integ
    ```
2.  **가상 환경 활성화:**
    *   Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    *   Linux/macOS:
        ```bash
        source ./.venv/bin/activate
        ```
3.  **필요한 Python 패키지 설치:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **`mcp_agent.py` 설정 변경:**
    *   `D:\workspace\agent_integ\src\mcp\mcp_agent.py` 파일을 엽니다.
    *   `RAG_API_URL`을 로컬 `rag` 서비스에 연결되도록 수정합니다:
        ```python
        RAG_API_URL = "http://localhost:8008/ask"
        ```

## 2. 서비스 실행 방법

### 2.1. `virtual_system` (WAS, Web) Docker로 실행

*   **새로운 터미널 창**을 엽니다.
*   `docker` 디렉토리로 이동합니다:
    ```bash
    cd D:\workspace\agent_integ\docker
    ```
*   Docker Compose를 실행합니다:
    ```bash
    docker-compose up --build -d
    ```
    ( `--build`는 이미지가 없거나 변경되었을 경우 빌드를 보장하고, `-d`는 백그라운드에서 실행합니다.)

### 2.2. `rag` 로컬에서 실행

*   **새로운 터미널 창**을 엽니다.
*   `rag` 서비스를 스크립트를 사용하여 실행합니다:
    ```bash
    D:\workspace\agent_integ\scripts\run_rag_local.bat
    ```
*   이 서비스는 일반적으로 `http://localhost:8008`에서 실행됩니다.

### 2.3. `mcp` 로컬에서 실행

*   또 다른 **새로운 터미널 창**을 엽니다.
*   Ollama 서버가 실행 중이고 `llama2` 모델이 사용 가능한지 확인합니다.
*   `mcp` 서비스를 스크립트를 사용하여 실행합니다:
    ```bash
    D:\workspace\agent_integ\scripts\run_mcp_local.bat
    ```
*   이 서비스는 일반적으로 `http://localhost:8000`에서 실행됩니다.

### 2.4. `was` 로컬에서 실행 (선택 사항, Docker 대신 로컬에서 실행하려는 경우)

*   또 다른 **새로운 터미널 창**을 엽니다.
*   `was` 서비스를 스크립트를 사용하여 실행합니다:
    ```bash
    D:\workspace\agent_integ\scripts\run_was_local.bat
    ```

## 3. 주요 파일 및 디렉토리

*   **`agent_integ/docker/docker-compose.yml`**: `virtual_system` (WAS, Web) 서비스 정의.
*   **`agent_integ/scripts/`**: 로컬에서 `mcp`, `rag`, `was` 서비스를 실행하기 위한 스크립트.
*   **`agent_integ/src/mcp/mcp_agent.py`**: MCP 서비스의 메인 애플리케이션.
*   **`agent_integ/src/rag/rag_service.py`**: RAG 서비스의 메인 애플리케이션.
*   **`agent_integ/src/virtual_system/was/app.py`**: WAS 서비스의 메인 애플리케이션.
*   **`agent_integ/src/virtual_system/web/`**: Web (Nginx) 서비스 관련 파일.
*   **`agent_integ/data/chroma_db`**: RAG 서비스에서 사용하는 ChromaDB 데이터.
*   **`agent_integ/data/db.json`**: WAS 서비스에서 사용하는 데이터베이스 파일.
