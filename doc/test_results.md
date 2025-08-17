### WAS 서비스 테스트

WAS 서비스는 `virtual_system` Docker Compose를 통해 실행되며, `web` 서비스(Nginx)를 통해 접근할 수 있습니다. `web` 서비스는 포트 80을 사용합니다.

**1. 작업 추가:**

새로운 할 일을 추가하려면 다음 `curl` 명령을 사용합니다:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"content": "새로운 할 일"}' http://localhost/api/tasks
```

**2. 작업 목록 조회:**

현재 할 일 목록을 조회하려면 다음 `curl` 명령을 사용합니다:
```bash
curl http://localhost/api/tasks
```

**예상 응답:**

작업 추가 시: 추가된 작업의 정보가 포함된 JSON 응답
작업 목록 조회 시: 현재 저장된 모든 작업의 목록이 포함된 JSON 배열

### RAG 서비스 테스트

RAG 서비스는 로컬에서 `http://localhost:8008` 포트로 실행됩니다. `/ask` 엔드포인트에 POST 요청을 보내 질문을 할 수 있습니다.

**1. 질문하기:**

다음 `curl` 명령을 사용하여 RAG 서비스에 질문을 보냅니다:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "인프라팀 역할이 뭐야?"}' http://localhost:8008/ask
```

**예상 응답:**

질문에 대한 RAG 시스템의 답변이 포함된 JSON 응답

### MCP 서비스 테스트

MCP 서비스는 로컬에서 `http://localhost:8000` 포트로 실행됩니다. `/ask` 엔드포인트에 POST 요청을 보내 사용자 질문을 전달할 수 있습니다. MCP는 LLM을 기반으로 질문의 의도를 파악하여 `WAS`, `RAG`, 또는 `COMBINED` 도구를 호출합니다.

**테스트 전 확인 사항:**
*   `WAS` 서비스 (Docker)가 실행 중이어야 합니다.
*   `RAG` 서비스 (로컬)가 실행 중이어야 합니다.
*   Ollama 서버가 실행 중이고 `llama2` 모델이 로드되어 있어야 합니다.

**1. WAS 도구 호출 테스트 (할 일 목록 조회):**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "현재 할 일 목록 보여줘"}' http://localhost:8000/ask
```

**2. RAG 도구 호출 테스트 (지식 검색):**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "인프라팀 역할이 뭐야?"}' http://localhost:8000/ask
```

**3. COMBINED 도구 호출 테스트 (RAG 기반 WAS 작업 추가):**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "인프라 미들웨어 변경 내역을 참고해서 '월간 인프라팀 보고서 작성' 할 일을 추가해줘"}' http://localhost:8000/ask
```

**예상 응답:**

각 쿼리에 대해 MCP가 호출한 도구의 응답이 JSON 형식으로 반환됩니다.

### WEB 서비스 테스트

WEB 서비스(Nginx)는 Docker Compose를 통해 실행되며, 포트 80을 통해 `WAS` 서비스로의 리버스 프록시 역할을 합니다.

**1. 웹 서비스 접근:**

다음 `curl` 명령을 사용하여 웹 서비스에 접근합니다. 이는 `WAS` 서비스의 기본 경로로 라우팅될 것입니다.
```bash
curl http://localhost/
```

**예상 응답:**

`WAS` 서비스의 기본 응답 (예: 빈 JSON 배열 `[]` 또는 초기 메시지)이 반환됩니다.

## 전체 시스템 통합 테스트 시나리오

이 섹션에서는 MCP 에이전트의 라우팅 및 도구 호출 기능을 포함한 전체 시스템의 통합 테스트 시나리오를 제시합니다. 테스트를 시작하기 전에 모든 서비스(`WAS`, `WEB`은 Docker로, `RAG`, `MCP`는 로컬로)가 실행 중인지 확인하십시오.

### 시나리오 1: 직접 RAG 쿼리 (지식 검색)

*   **목표:** MCP가 사용자 질문을 `RAG` 도구로 올바르게 라우팅하고, `RAG` 서비스가 답변을 반환하는지 확인합니다.
*   **명령:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "인프라팀 역할이 뭐야?"}' http://localhost:8000/ask
    ```
*   **예상 결과:** `RAG` 서비스에서 반환된 답변이 포함된 JSON 응답.

### 시나리오 2: 직접 WAS 쿼리 (할 일 목록 조회)

*   **목표:** MCP가 사용자 질문을 `WAS` 도구로 올바르게 라우팅하고, `WAS` 서비스가 할 일 목록을 반환하는지 확인합니다.
*   **명령:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "현재 할 일 목록 보여줘"}' http://localhost:8000/ask
    ```
*   **예상 결과:** `WAS` 서비스에서 반환된 할 일 목록이 포함된 JSON 응답.

### 시나리오 3: 직접 WAS 쿼리 (할 일 추가)

*   **목표:** MCP가 사용자 질문을 `WAS` 도구로 올바르게 라우팅하고, `WAS` 서비스가 새로운 할 일을 성공적으로 추가하는지 확인합니다.
*   **명령:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "'새로운 통합 테스트 계획' 할 일을 추가해줘"}' http://localhost:8000/ask
    ```
*   **예상 결과:** `WAS` 서비스에서 반환된 추가된 할 일 정보가 포함된 JSON 응답.

### 시나리오 4: 복합 쿼리 (RAG 기반 WAS 작업 추가)

*   **목표:** MCP가 사용자 질문을 `COMBINED` 도구로 올바르게 라우팅하고, `RAG` 서비스의 답변을 기반으로 `WAS` 서비스에 할 일을 추가하는지 확인합니다.
*   **명령:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "인프라 미들웨어 변경 내역을 참고해서 '월간 인프라팀 보고서 작성' 할 일을 추가해줘"}' http://localhost:8000/ask
    ```
*   **예상 결과:** `WAS` 서비스에서 반환된 추가된 할 일 정보가 포함된 JSON 응답. 이 할 일 내용은 `RAG` 서비스의 답변을 기반으로 생성됩니다.
