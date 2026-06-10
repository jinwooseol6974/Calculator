import streamlit as st
import random
import numpy as np
import math

st.set_page_config(page_title="World Cup Simulator", page_icon="🏆", layout="wide")

# =========================
# MODE SELECT
# =========================

mode = st.sidebar.radio("모드 선택", ["계산기", "월드컵 시뮬레이터"])

# =========================
# CALCULATOR
# =========================

def calculator():
    st.title("🧮 계산기")

    op = st.selectbox("연산", ["+", "-", "*", "/", "%", "**", "log"])

    if op != "log":
        a = st.number_input("A", value=1.0)
        b = st.number_input("B", value=1.0)
    else:
        a = st.number_input("값", value=10.0, min_value=0.0001)
        b = st.number_input("밑", value=10.0, min_value=0.0001)

    if st.button("계산"):
        if op == "+":
            r = a + b
        elif op == "-":
            r = a - b
        elif op == "*":
            r = a * b
        elif op == "/":
            r = a / b if b != 0 else 0
        elif op == "%":
            r = a % b
        elif op == "**":
            r = a ** b
        elif op == "log":
            r = math.log(a, b)

        st.success(f"결과: {r}")


# =========================
# WORLD CUP DATA
# =========================

teams = {
    "France": 1, "Brazil": 2, "Argentina": 3, "England": 4,
    "Spain": 5, "Germany": 6, "Portugal": 7, "Netherlands": 8,
    "Belgium": 9, "Italy": 10, "Croatia": 11, "Uruguay": 12,
    "USA": 13, "Mexico": 14, "Canada": 15, "Japan": 16,
    "Korea": 17, "Morocco": 18, "Senegal": 19, "Switzerland": 20,
    "Denmark": 21, "Poland": 22, "Austria": 23, "Australia": 24,
    "Ecuador": 25, "Colombia": 26, "Chile": 27, "Peru": 28,
    "Nigeria": 29, "Egypt": 30, "Ghana": 31, "Iran": 32,
    "Saudi Arabia": 33, "Qatar": 34, "South Africa": 35, "Tunisia": 36,
    "Serbia": 37, "Ukraine": 38, "Turkey": 39, "Norway": 40,
    "Wales": 41, "Scotland": 42, "Costa Rica": 43, "Panama": 44,
    "New Zealand": 45, "Iceland": 46, "Finland": 47, "Hungary": 48
}

GROUPS = [chr(i) for i in range(65, 77)]  # A-L


# =========================
# STRENGTH MODEL
# =========================

def strength(rank):
    return 2100 - rank * 8


def win_prob(a, b):
    ra, rb = strength(a), strength(b)
    return 1 / (1 + 10 ** ((rb - ra) / 400))


# =========================
# MATCH SIMULATION
# =========================

def simulate_score(t1, t2):
    s1, s2 = strength(teams[t1]), strength(teams[t2])
    total = s1 + s2

    xg1 = 0.3 + 2.5 * (s1 / total)
    xg2 = 0.3 + 2.5 * (s2 / total)

    g1 = np.random.poisson(xg1)
    g2 = np.random.poisson(xg2)

    return g1, g2


# =========================
# PENALTY
# =========================

def penalty(t1, t2):
    p1 = win_prob(teams[t1], teams[t2])

    s1 = s2 = 0
    for i in range(5):
        if random.random() < p1:
            s1 += 1
        if random.random() < (1 - p1):
            s2 += 1

    while s1 == s2:
        if random.random() < p1:
            s1 += 1
        else:
            s2 += 1

    return s1, s2


# =========================
# KNOCKOUT MATCH
# =========================

def knockout(t1, t2):
    g1, g2 = simulate_score(t1, t2)

    if g1 > g2:
        return t1, g1, g2, "90min"
    if g2 > g1:
        return t2, g1, g2, "90min"

    e1, e2 = simulate_score(t1, t2)
    g1 += e1
    g2 += e2

    if g1 > g2:
        return t1, g1, g2, "ET"
    if g2 > g1:
        return t2, g1, g2, "ET"

    p1, p2 = penalty(t1, t2)
    winner = t1 if p1 > p2 else t2

    return winner, g1, g2, f"PK {p1}-{p2}"


# =========================
# GROUP STAGE
# =========================

def create_groups():
    teams_list = list(teams.keys())
    random.shuffle(teams_list)

    groups = {}
    for i, g in enumerate(GROUPS):
        groups[g] = teams_list[i*4:(i+1)*4]

    return groups


def play_group(group_teams):
    table = {t: {"pts":0,"gf":0,"ga":0,"gd":0} for t in group_teams}

    matches = [
        (0,1),(2,3),
        (0,2),(1,3),
        (0,3),(1,2)
    ]

    for a,b in matches:
        t1, t2 = group_teams[a], group_teams[b]
        g1, g2 = simulate_score(t1, t2)

        table[t1]["gf"] += g1
        table[t1]["ga"] += g2
        table[t2]["gf"] += g2
        table[t2]["ga"] += g1

        if g1 > g2:
            table[t1]["pts"] += 3
        elif g2 > g1:
            table[t2]["pts"] += 3
        else:
            table[t1]["pts"] += 1
            table[t2]["pts"] += 1

    for t in table:
        table[t]["gd"] = table[t]["gf"] - table[t]["ga"]

    return sorted(
        table.items(),
        key=lambda x: (x[1]["pts"], x[1]["gd"], x[1]["gf"]),
        reverse=True
    )


# =========================
# TOURNAMENT
# =========================

def tournament(teams_list):
    round_names = ["32강","16강","8강","4강","결승"]

    round_i = 0

    while len(teams_list) > 1:
        st.subheader(round_names[round_i])
        round_i += 1

        winners = []

        for i in range(0, len(teams_list), 2):
            t1, t2 = teams_list[i], teams_list[i+1]
            w, g1, g2, mode = knockout(t1, t2)

            st.write(f"{t1} {g1}-{g2} {t2} → 🏆 {w} ({mode})")
            winners.append(w)

        teams_list = winners

    return teams_list[0]


# =========================
# WORLD CUP MODE
# =========================

def worldcup():
    st.title("🏆 2026 월드컵 시뮬레이터")

    if st.button("🎲 조 추첨 + 시작"):

        groups = create_groups()

        qualified = []

        st.subheader("📦 조별리그")

        for g, teams_list in groups.items():

            st.write(f"### Group {g}")
            result = play_group(teams_list)

            for i, (team, stat) in enumerate(result):
                st.write(f"{i+1}. {team} {stat['pts']}pt")

            # 4조 2팀, 8조 3팀 진출
            if g in ["A","B","C","D"]:
                qualified += [r[0] for r in result[:2]]
            else:
                qualified += [r[0] for r in result[:3]]

        random.shuffle(qualified)

        st.subheader("🏆 토너먼트")

        champion = tournament(qualified)

        st.success(f"🏆 우승: {champion}")

        st.balloons()


# =========================
# RUN
# =========================

if mode == "계산기":
    calculator()
else:
    worldcup()    "Denmark": 20,
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
