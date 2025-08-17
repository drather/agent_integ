import requests
import json
import re
from langchain_community.llms import Ollama
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

# --- MCP 라우터용 LLM 인스턴스 ---
# 이 LLM은 MCP가 라우팅 결정을 내리는 데 사용됩니다.
# Ollama 서버가 'llama2' 모델과 함께 실행 중인지 확인해주세요.
try:
    mcp_llm = Ollama(model="llama2", temperature=0.1)
    print("MCP 라우터 LLM (Ollama) 로드 성공.")
except Exception as e:
    print(f"MCP 라우터 LLM 로드 오류: {e}. Ollama 서버가 실행 중인지 확인해주세요.")
    mcp_llm = None

# Phase 1에서 만든 WAS API 주소 (Docker로 실행되고 Nginx를 통해 80번 포트로 접근)
WAS_API_URL = "http://127.0.0.1/api/tasks"

# RAG API 주소
RAG_API_URL = "http://localhost:8008/ask"

# --- LLM을 위한 도구 설명 ---
TOOL_DESCRIPTIONS = """
Available Tools:
- **WAS_API**: Manages 'tasks' or 'to-do' items.
    - **Actions**: 'list' (to get all tasks), 'add' (to add a new task).
    - **Parameters for 'add'**: `content` (string, required) - The description of the task to add.
    - Example JSON response for 'list': {"tool": "WAS_API", "action": "list"}
    - Example JSON response for 'add': {"tool": "WAS_API", "action": "add", "parameters": {"content": "회의록 작성"}}

- **RAG**: Answers questions based on documents or general knowledge.
    - **Parameters**: `query` (string, required) - The question to ask the RAG system.
    - Example JSON response: {"tool": "RAG", "parameters": {"query": "인프라팀 역할이 뭐야?"}}

- **COMBINED**: Performs a task that requires both RAG and WAS_API.
    - This tool is used when the user asks to perform a task (WAS_API) but also explicitly references external information or documents (RAG) as a basis for the task.
    - **Parameters**: `query` (string, required) - The original user query for the combined task.
    - Example JSON response: {"tool": "COMBINED", "parameters": {"query": "인프라 미들웨어 변경 내역을 참고해서 '월간 인프라팀 보고서 작성' 할 일을 추가해줘"}}

Your task is to decide which tool and action is most appropriate for the user's query, and extract any necessary parameters.
Respond with a JSON string only, like the examples above.
"""

# --- WAS API 호출 함수 (액션별 분리) ---
def call_was_api_list():
    """WAS API를 호출하여 할 일 목록을 조회합니다."""
    print(">>> 도구: WAS API 호출 (목록 조회)")
    try:
        response = requests.get(WAS_API_URL)
        response.raise_for_status()
        return f"WAS API 응답 (작업 목록): {response.json()}"
    except requests.exceptions.RequestException as e:
        return f"WAS API 호출 오류: {e}"

def call_was_api_add(content: str):
    """WAS API를 호출하여 새로운 할 일을 추가합니다."""
    print(">>> 도구: WAS API 호출 (할 일 추가)")
    try:
        response = requests.post(WAS_API_URL, json={'content': content})
        response.raise_for_status()
        return f"WAS API 응답 (작업 추가): {response.json()}"
    except requests.exceptions.RequestException as e:
        return f"WAS API 호출 오류: {e}"

# --- RAG API 호출 함수 ---
def call_rag_system(query: str):
    """
    지식 검색(RAG) API를 호출하는 도구
    """
    print(">>> 도구: RAG 시스템 호출")
    try:
        response = requests.post(RAG_API_URL, json={'query': query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"RAG API 호출 오류: {e}"}

# --- 복합 작업 실행 함수 ---
def run_combined_task(query: str):
    """
    RAG 검색 결과에 기반하여 WAS 작업을 수행하는 복합 도구
    """
    print(">>> 복합 작업 실행: RAG 검색 -> WAS 작업 추가")
    
    print("1단계: RAG 시스템에서 정보 검색...")
    rag_response = call_rag_system(query)
    rag_answer = rag_response.get('answer', 'RAG에서 답변을 찾지 못했습니다.')
    
    print(f"\n--- RAG 전체 답변 확인 ---\n{rag_answer}\n--------------------------\n")
    
    print("2단계: RAG 답변을 기반으로 새 작업 내용 생성...")
    task_content = "RAG 기반 작업"
    match = re.search(r"'(.*?)'", query)
    if match:
        task_content = match.group(1)
        
    new_task_description = f"'{task_content}' (근거: {rag_answer[:80]}...)"
    
    print(f"3단계: 생성된 내용으로 WAS에 작업 추가 요청...")
    return call_was_api_add(new_task_description) # call_was_api_add로 변경


# --- 메인 라우터 함수 ---
def router(query: str):
    """
    LLM을 활용하여 사용자 질문의 의도를 파악하고 적절한 도구를 호출하는 라우터
    """
    print(f"\n[사용자 질문] \"{query}\"")
    
    if mcp_llm is None:
        return "오류: MCP 라우터 LLM이 로드되지 않았습니다. Ollama 서버를 확인해주세요."

    # LLM에게 라우팅 결정을 요청하는 프롬프트
    routing_prompt = f"""
    {TOOL_DESCRIPTIONS}

    User Query: "{query}"

    Based on the User Query, respond with a JSON string only, indicating the tool, action, and parameters.
    """
    
    print(">>> LLM에게 라우팅 결정 요청...")
    llm_response_str = mcp_llm.invoke(routing_prompt).strip()
    print(f">>> LLM 응답: {llm_response_str}")

    try:
        llm_decision = json.loads(llm_response_str)
        tool_name = llm_decision.get("tool", "").upper()
        action = llm_decision.get("action", "")
        parameters = llm_decision.get("parameters", {})

        if tool_name == "WAS_API":
            if action == "list":
                return call_was_api_list()
            elif action == "add":
                content = parameters.get("content")
                if content:
                    return call_was_api_add(content)
                else:
                    return "오류: WAS_API 'add' 액션에 'content' 파라미터가 누락되었습니다."
            else:
                return f"오류: WAS_API에 알 수 없는 액션: {action}"
        elif tool_name == "RAG":
            rag_query = parameters.get("query")
            if rag_query:
                return call_rag_system(rag_query)
            else:
                return "오류: RAG 도구에 'query' 파라미터가 누락되었습니다."
        elif tool_name == "COMBINED":
            combined_query = parameters.get("query")
            if combined_query:
                return run_combined_task(combined_query)
            else:
                return "오류: COMBINED 도구에 'query' 파라미터가 누락되었습니다."
        else:
            return f"오류: LLM이 알 수 없는 도구를 결정했습니다: {tool_name}"
    except json.JSONDecodeError:
        return f"오류: LLM 응답이 유효한 JSON 형식이 아닙니다: {llm_response_str}"
    except Exception as e:
        return f"라우팅 중 예외 발생: {e}"

# --- FastAPI 애플리케이션 인스턴스 ---
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_mcp(request: QueryRequest):
    """
    사용자 질문을 받아 MCP 라우터를 통해 처리하고 응답을 반환합니다.
    """
    response = router(request.query)
    return {"answer": response}

if __name__ == "__main__":
    # 이 부분은 Docker 컨테이너 내에서 Uvicorn이 직접 실행하므로,
    # 로컬 테스트용으로만 사용됩니다.
    print("MCP Agent API 모드로 실행합니다. (http://0.0.0.0:8000)")
    uvicorn.run(app, host="0.0.0.0", port=8000)