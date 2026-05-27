import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 💖\n"
                "연애 고민을 편하게 이야기해주세요.\n"
                "공감과 현실적인 조언을 함께 드릴게요."
            )
        }
    ]

# 기존 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("연애 고민을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini 대화 형식 변환
            contents = []

            for msg in st.session_state.messages:
                role = "model" if msg["role"] == "assistant" else "user"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            system_prompt = """
당신은 따뜻하고 공감 능력이 높은 연애상담 AI입니다.

규칙:
- 공감하는 말투 사용
- 현실적인 조언 제공
- 지나친 단정 금지
- 공격적 표현 금지
- 답변은 자연스럽고 친근하게
- 한국어로 답변
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.8,
                    max_output_tokens=700
                )
            )

            bot_reply = response.text

            # 응답 출력
            message_placeholder.markdown(bot_reply)

            # 응답 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": bot_reply
                }
            )

        except Exception as e:
            error_message = f"오류가 발생했어요 😢\n\n{str(e)}"

            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )
