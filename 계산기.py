# app.py
# Streamlit 계산기 웹앱

import streamlit as st
import math

st.set_page_config(page_title="다기능 계산기", page_icon="🧮")

st.title("🧮 다기능 계산기 웹앱")

st.write("사칙연산, 모듈러연산, 지수연산, 로그연산을 지원합니다.")

# 연산 선택
operation = st.selectbox(
    "원하는 연산을 선택하세요.",
    (
        "덧셈",
        "뺄셈",
        "곱셈",
        "나눗셈",
        "모듈러연산",
        "지수연산",
        "로그연산"
    )
)

# 숫자 입력
if operation != "로그연산":
    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)

