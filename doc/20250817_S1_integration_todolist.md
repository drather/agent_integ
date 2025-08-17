# Agent Integration Project Todo-List (S1)

> 기존 RAG PoC와 MCP PoC를 통합하여 LLM 에이전트 기반의 멀티 모듈 서비스로 재구축 계획

## Phase 1: 프로젝트 구조 정의 및 초기화

- [x] **새로운 디렉토리 구조 생성**
    - [x] `agent_integ/src/mcp` (MCP 로직)
    - [x] `agent_integ/src/rag` (RAG 로직)
    - [x] `agent_integ/src/virtual_system` (WEB/WAS/DB 가상 시스템)
    - [x] `agent_integ/shared` (공통 유틸리티, 모델 등)
    - [x] `agent_integ/docker` (Docker 관련 파일)

- [x] **통합된 가상 환경 설정**
    - [x] `agent_integ/.venv` 생성 및 활성화

- [x] **통합된 의존성 파일 (`requirements.txt`) 생성**
    - [x] 모든 모듈의 의존성을 포함하는 단일 `requirements.txt` 작성

## Phase 2: 기존 코드 마이그레이션

- [x] **`rag_poc` 코드 이동 및 통합**
    - [x] `rag_poc/rag_poc.py` -> `agent_integ/src/rag/rag_service.py`
    - [x] `rag_poc/chroma_db` -> `agent_integ/data/chroma_db` (데이터 폴더 분리)
    - [x] `rag_poc/models` -> `agent_integ/models` (모델 폴더 분리)

- [x] **`mcp_poc` 코드 이동 및 통합**
    - [x] `mcp_poc/mcp_server/app.py` -> `agent_integ/src/mcp/mcp_agent.py`
    - [x] `mcp_poc/db/db.json` -> `agent_integ/data/db.json`

- [x] **`web/was/db` 가상 시스템 코드 이동 및 통합**
    - [x] `mcp_poc/was` -> `agent_integ/src/virtual_system/was`
    - [x] `mcp_poc/web` -> `agent_integ/src/virtual_system/web`

## Phase 3: LLM 에이전트 로직 구현 (MCP 고도화)

- [x] **LLM 기반 라우터/플래너 구현**
    - [x] `mcp_agent.py` 내에서 LLM을 활용하여 사용자 요청의 의도 파악 및 다단계 실행 계획 수립

- [x] **도구(Tool) 정의 및 LLM 연동**
    - [x] `rag_service.py`의 RAG API를 LLM 에이전트의 도구로 정의
    - [x] `virtual_system/was`의 WAS API를 LLM 에이전트의 도구로 정의
    - [x] LLM이 도구 사용 시 필요한 파라미터 추출 로직 구현

- [x] **서비스 간 통신 설정**
    - [x] Docker 네트워크를 통한 모듈 간 통신 설정

## Phase 4: Docker Orchestration 재구성

- [x] **통합된 `Dockerfile` 및 `docker-compose.yml` 작성**
    - [x] 각 모듈별 `Dockerfile` (예: `src/mcp/Dockerfile`, `src/rag/Dockerfile`)
    - [x] 전체 서비스를 통합하는 `docker-compose.yml` 작성

- [x] **서비스 간 통신 설정**
    - [x] Docker 네트워크를 통한 모듈 간 통신 설정

## Phase 5: 통합 테스트 및 디버깅

- [ ] **각 컴포넌트별 테스트**
    - [ ] 마이그레이션된 각 모듈의 독립적인 기능 테스트

- [x] **전체 시스템 통합 테스트 시나리오 작성 및 실행**
    - [ ] LLM 에이전트의 복합적인 요청 처리 능력 검증

## Phase 6: 문서화 및 정리

- [x] **프로젝트 구조 및 구현 상세 문서화**
    - `setup_guide.md` 및 `test_results.md` 파일에 개발 환경 설정, 서비스 실행 방법, 컴포넌트별 및 통합 테스트 시나리오가 상세히 문서화되었습니다.

- [x] **향후 발전 방향 및 개선점 도출**
    - **오류 처리 및 견고성:** 서비스, 특히 외부 API 호출(RAG, WAS)에서 더 포괄적인 오류 처리 로직을 구현하여 시스템의 안정성을 높일 수 있습니다.
    - **로깅 및 모니터링:** 구조화된 로깅 시스템과 모니터링 도구를 도입하여 시스템의 동작을 더 잘 관찰하고 문제를 신속하게 파악할 수 있습니다.
    - **성능 최적화:** LLM 호출, RAG 검색, 데이터 처리 등 성능 병목 지점을 식별하고 최적화하여 응답 시간을 단축할 수 있습니다.
    - **확장성:** 프로덕션 환경 배포를 위해 컨테이너 오케스트레이션(예: Kubernetes) 도입을 고려하여 서비스의 확장성과 가용성을 확보할 수 있습니다.
    - **고급 LLM 기능:** 더 정교한 프롬프트 엔지니어링 기법, Few-shot 학습, 또는 특정 도메인에 대한 LLM 미세 조정을 탐색하여 에이전트의 지능과 성능을 향상시킬 수 있습니다.
    - **보안:** API에 대한 인증/권한 부여 메커니즘을 구현하여 시스템의 보안을 강화할 수 있습니다.
    - **CI/CD:** 지속적인 통합 및 배포(CI/CD) 파이프라인을 구축하여 개발 프로세스의 효율성과 배포의 안정성을 높일 수 있습니다.
    - **자동화된 테스트 확장:** 현재의 수동 테스트 외에, Pytest와 같은 적절한 테스트 프레임워크를 사용하여 단위 테스트 및 통합 테스트 스위트를 확장하여 코드 변경에 대한 회귀를 방지할 수 있습니다.


## Current Setup and Execution Guide

프로젝트의 통합 및 실행 방식이 다음과 같이 최종 확정되었습니다.

*   **`mcp` 및 `rag` 서비스**: GPU 사용 및 개발 편의성을 위해 로컬 Python 프로세스로 실행됩니다.
*   **`virtual_system` (WAS, Web) 서비스**: Docker 컨테이너로 실행됩니다.

자세한 설정 방법 및 서비스 실행 지침은 다음 문서를 참조하십시오:
[개발 환경 설정 및 서비스 실행 가이드](setup_guide.md)

**주요 변경 사항 요약:**

*   `agent_integ/src/mcp/mcp_agent.py` 내 `RAG_API_URL`이 `http://localhost:8008/ask`로 변경되었습니다.
*   `agent_integ/scripts/` 디렉토리에 각 로컬 서비스(`mcp`, `rag`, `was`)를 실행하는 스크립트가 추가되었습니다.
*   `docker-compose.yml`은 `virtual_system` (WAS, Web) 서비스만 관리하도록 재구성되었습니다.
*   `rag_poc/models`는 더 이상 사용되지 않으며, `rag` 서비스는 Ollama를 통해 외부 LLM을 사용합니다.
