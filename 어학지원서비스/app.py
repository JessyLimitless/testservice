import streamlit as st
import openai

# OpenAI API 키 입력 필드
st.title("한국어 ↔ 베트남어 번역 서비스")

api_key_input = st.text_input("OpenAI API 키를 입력하세요", type="password")

# st.session_state를 사용해 대화 기록 관리
if 'history' not in st.session_state:
    st.session_state['history'] = []

# 사용자가 API 키를 입력했는지 확인
if api_key_input:
    openai.api_key = api_key_input

    # 텍스트 입력 필드
    input_text = st.text_area("번역할 한국어 또는 베트남어 텍스트를 입력하세요", height=150)

    # 번역 버튼
    if st.button("번역하기"):
        if input_text:
            try:
                # GPT-3.5-turbo 모델을 사용한 번역 요청 (베트남어 ↔ 한국어)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Translate the following text between Korean and Vietnamese."},
                        {"role": "user", "content": input_text}
                    ]
                )

                # 번역 결과 저장 및 표시
                translation = response.choices[0].message['content']
                st.session_state['history'].append({"input": input_text, "output": translation})

                # 번역 결과 출력 (스타일링 추가)
                st.write("### 번역된 결과:")
                st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #007BFF;'>{translation}</div>", unsafe_allow_html=True)

                # 주요 단어 설명 및 유사 문장 (한국어와 베트남어로 제공)
                st.write("### 추가 정보:")
                explanation_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "For the following translated text, provide explanations for key terms in both Korean and Vietnamese, and offer similar example sentences in both languages."},
                        {"role": "user", "content": translation}
                    ]
                )
                explanation = explanation_response.choices[0].message['content']
                st.write(explanation)

            except openai.error.AuthenticationError:
                st.error("API 키가 올바르지 않습니다. 다시 확인해 주세요.")
        else:
            st.warning("번역할 텍스트를 입력하세요.")

    # 대화 기록 초기화 버튼
    if st.button("대화 기록 초기화"):
        st.session_state['history'] = []

    # 대화 기록 표시
    if st.session_state['history']:
        st.write("## 대화 기록")
        for idx, entry in enumerate(st.session_state['history']):
            st.write(f"**{idx+1}. 입력:** {entry['input']}")
            st.write(f"**번역:** <span style='color: #28A745;'>{entry['output']}</span>", unsafe_allow_html=True)
            st.write("---")
else:
    st.warning("API 키를 입력하세요.")
