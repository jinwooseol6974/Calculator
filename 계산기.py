# app.py

import streamlit as st
import math
import random

st.set_page_config(
    page_title="다기능 계산기 & 월드컵 시뮬레이터",
    page_icon="🧮",
    layout="wide"
)

# =========================
# FIFA 랭킹 데이터
# =========================

teams = {
    "France": 1,
    "Spain": 2,
    "Argentina": 3,
    "England": 4,
    "Portugal": 5,
    "Brazil": 6,
    "Netherlands": 7,
    "Morocco": 8,
    "Belgium": 9,
    "Germany": 10,
    "Croatia": 11,
    "Italy": 12,
    "Colombia": 13,
    "Senegal": 14,
    "Mexico": 15,
    "USA": 16,
    "Uruguay": 17,
    "Japan": 18,
    "Switzerland": 19,
    "Denmark": 20,
    "Austria": 22,
    "South Korea": 25,
    "Australia": 27,
    "Canada": 30,
    "Poland": 35,
    "Serbia": 32,
    "Turkey": 28,
    "Iran": 21,
    "Ukraine": 24,
    "Sweden": 26,
    "Norway": 38,
    "Chile": 42
}

# =========================
# 사이드바 메뉴
# =========================

st.sidebar.title("⚙️ 메뉴")

mode = st.sidebar.radio(
    "모드 선택",
    ["계산기", "월드컵 시뮬레이터"]
)

# =========================
# 계산기 모드
# =========================

if mode == "계산기":

    st.title("🧮 다기능 계산기")

    st.write(
        "사칙연산, 모듈러연산, 지수연산, 로그연산을 지원합니다."
    )

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

    if operation != "로그연산":
        num1 = st.number_input(
            "첫 번째 숫자",
            value=0.0
        )

        num2 = st.number_input(
            "두 번째 숫자",
            value=0.0
        )

    else:
        num1 = st.number_input(
            "로그를 구할 숫자",
            min_value=0.0001,
            value=10.0
        )

        num2 = st.number_input(
            "로그의 밑",
            min_value=0.0001,
            value=10.0
        )

    if st.button("계산하기"):

        try:

            if operation == "덧셈":
                result = num1 + num2

            elif operation == "뺄셈":
                result = num1 - num2

            elif operation == "곱셈":
                result = num1 * num2

            elif operation == "나눗셈":

                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()

                result = num1 / num2

            elif operation == "모듈러연산":

                if num2 == 0:
                    st.error("0으로 나눈 나머지는 계산할 수 없습니다.")
                    st.stop()

                result = num1 % num2

            elif operation == "지수연산":
                result = num1 ** num2

            elif operation == "로그연산":

                if num1 <= 0:
                    st.error("로그 값은 0보다 커야 합니다.")
                    st.stop()

                if num2 <= 0 or num2 == 1:
                    st.error("밑은 0보다 크고 1이 아니어야 합니다.")
                    st.stop()

                result = math.log(num1, num2)

            st.success(f"결과: {result}")

        except Exception as e:
            st.error(f"오류 발생: {e}")

# =========================
# 월드컵 시뮬레이터 모드
# =========================

elif mode == "월드컵 시뮬레이터":

    st.title("🏆 FIFA 월드컵 토너먼트 시뮬레이터")

    st.write(
        "FIFA 랭킹을 기반으로 각 팀의 승리 확률을 계산하여 토너먼트를 진행합니다."
    )

    # Elo 스타일 승률 계산
    def win_probability(rank_a, rank_b):

        rating_a = 2100 - rank_a * 8
        rating_b = 2100 - rank_b * 8

        return 1 / (
            1 + 10 ** ((rating_b - rating_a) / 400)
        )

    # 경기 시뮬레이션
    def simulate_match(team1, team2):

        p = win_probability(
            teams[team1],
            teams[team2]
        )

        if random.random() < p:
            return team1
        else:
            return team2

    # 토너먼트 진행
    def simulate_tournament(team_list):

        round_names = {
            16: "16강",
            8: "8강",
            4: "4강",
            2: "결승"
        }

        while len(team_list) > 1:

            st.subheader(round_names[len(team_list)])

            winners = []

            for i in range(0, len(team_list), 2):

                team1 = team_list[i]
                team2 = team_list[i + 1]

                winner = simulate_match(
                    team1,
                    team2
                )

                losers = team2 if winner == team1 else team1

                prob = win_probability(
                    teams[team1],
                    teams[team2]
                )

                if winner == team2:
                    prob = 1 - prob

                st.write(
                    f"⚽ {team1} vs {team2} → "
                    f"🏆 **{winner}** "
                    f"(승리확률 {prob:.1%})"
                )

                winners.append(winner)

            st.divider()

            team_list = winners

        return team_list[0]

    default_teams = list(teams.keys())[:16]

    selected_teams = st.multiselect(
        "참가 국가를 선택하세요 (정확히 16개)",
        list(teams.keys()),
        default=default_teams
    )

    st.info(
        f"현재 선택된 국가 수: {len(selected_teams)}"
    )

    if len(selected_teams) != 16:
        st.warning("반드시 16개 국가를 선택해야 합니다.")
    else:

        if st.button("🚀 시뮬레이션 시작"):

            shuffled = selected_teams.copy()
            random.shuffle(shuffled)

            st.subheader("🎲 대진표")

            for i in range(0, len(shuffled), 2):
                st.write(
                    f"{shuffled[i]} vs {shuffled[i+1]}"
                )

            st.divider()

            champion = simulate_tournament(
                shuffled
            )

            st.success(
                f"🏆 최종 우승국: {champion}"
            )

            st.balloons()
