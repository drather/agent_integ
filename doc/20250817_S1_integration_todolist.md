# Agent Integration Project Todo-List (S1)

> 기존 RAG PoC와 MCP PoC를 통합하여 LLM 에이전트 기반의 멀티 모듈 서비스로 재구축 계획

## Phase 1: 프로젝트 구조 정의 및 초기화

- [ ] **새로운 디렉토리 구조 생성**
    - [ ] `agent_integ/src/mcp` (MCP 로직)
    - [ ] `agent_integ/src/rag` (RAG 로직)
    - [ ] `agent_integ/src/virtual_system` (WEB/WAS/DB 가상 시스템)
    - [ ] `agent_integ/shared` (공통 유틸리티, 모델 등)
    - [ ] `agent_integ/docker` (Docker 관련 파일)

- [ ] **통합된 가상 환경 설정**
    - [ ] `agent_integ/.venv` 생성 및 활성화

- [ ] **통합된 의존성 파일 (`requirements.txt`) 생성**
    - [ ] 모든 모듈의 의존성을 포함하는 단일 `requirements.txt` 작성

## Phase 2: 기존 코드 마이그레이션

- [ ] **`rag_poc` 코드 이동 및 통합**
    - [ ] `rag_poc/rag_poc.py` -> `agent_integ/src/rag/rag_service.py`
    - [ ] `rag_poc/chroma_db` -> `agent_integ/data/chroma_db` (데이터 폴더 분리)
    - [ ] `rag_poc/models` -> `agent_integ/models` (모델 폴더 분리)

- [ ] **`mcp_poc` 코드 이동 및 통합**
    - [ ] `mcp_poc/mcp_server/app.py` -> `agent_integ/src/mcp/mcp_agent.py`
    - [ ] `mcp_poc/db/db.json` -> `agent_integ/data/db.json`

- [ ] **`web/was/db` 가상 시스템 코드 이동 및 통합**
    - [ ] `mcp_poc/was` -> `agent_integ/src/virtual_system/was`
    - [ ] `mcp_poc/web` -> `agent_integ/src/virtual_system/web`

## Phase 3: LLM 에이전트 로직 구현 (MCP 고도화)

- [ ] **LLM 기반 라우터/플래너 구현**
    - [ ] `mcp_agent.py` 내에서 LLM을 활용하여 사용자 요청의 의도 파악 및 다단계 실행 계획 수립

- [ ] **도구(Tool) 정의 및 LLM 연동**
    - [ ] `rag_service.py`의 RAG API를 LLM 에이전트의 도구로 정의
    - [ ] `virtual_system/was`의 WAS API를 LLM 에이전트의 도구로 정의
    - [ ] LLM이 도구 사용 시 필요한 파라미터 추출 로직 구현

## Phase 4: Docker Orchestration 재구성

- [ ] **통합된 `Dockerfile` 및 `docker-compose.yml` 작성**
    - [ ] 각 모듈별 `Dockerfile` (예: `src/mcp/Dockerfile`, `src/rag/Dockerfile`)
    - [ ] 전체 서비스를 통합하는 `docker-compose.yml` 작성

- [ ] **서비스 간 통신 설정**
    - [ ] Docker 네트워크를 통한 모듈 간 통신 설정

## Phase 5: 통합 테스트 및 디버깅

- [ ] **각 컴포넌트별 테스트**
    - [ ] 마이그레이션된 각 모듈의 독립적인 기능 테스트

- [ ] **전체 시스템 통합 테스트 시나리오 작성 및 실행**
    - [ ] LLM 에이전트의 복합적인 요청 처리 능력 검증

## Phase 6: 문서화 및 정리

- [ ] **프로젝트 구조 및 구현 상세 문서화**
- [ ] **향후 발전 방향 및 개선점 도출**
