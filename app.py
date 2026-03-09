import streamlit as st
import itertools
import pandas as pd

st.set_page_config(page_title="LaLaLa式・裏読みAI PRO", layout="wide")

st.title("🏇 LaLaLa式・究極の裏読みAI PRO")

# ----------------------------
# オッズ入力
# ----------------------------

st.sidebar.header("① 5大オッズ")

w_o = st.sidebar.number_input("単勝", value=1.5, step=0.1)
qr_o = st.sidebar.number_input("馬連", value=3.5, step=0.1)
ex_o = st.sidebar.number_input("馬単", value=7.0, step=0.1)
tr_o = st.sidebar.number_input("3連複", value=8.0, step=0.1)
tf_o = st.sidebar.number_input("3連単", value=15.0, step=1.0)

# ----------------------------
# 記事評価
# ----------------------------

st.sidebar.header("② 一番人気の評判")

sentiment = st.sidebar.selectbox(
    "記事トーン",
    ["絶賛（死角なし）", "普通（一長一短）", "不安（疑問あり）"]
)

# ----------------------------
# 馬番入力
# ----------------------------

st.sidebar.header("③ 馬番")

h_in = st.sidebar.text_input(
    "馬番をカンマ区切り",
    "1,2,3,4,5,6,7,8,9,10"
)

h_list = [h.strip() for h in h_in.split(",") if h.strip() != ""]

if len(h_list) < 5:
    st.error("5頭以上入力してください")
    st.stop()

if len(set(h_list)) != len(h_list):
    st.error("馬番が重複しています")
    st.stop()

# ----------------------------
# 印
# ----------------------------

st.sidebar.header("④ LaLaLa印")

m1 = st.sidebar.selectbox("◎", h_list, 0)
m2 = st.sidebar.selectbox("○", h_list, 1)
m3 = st.sidebar.selectbox("▲", h_list, 2)
m4 = st.sidebar.selectbox("△", h_list, 3)
m5 = st.sidebar.selectbox("×", h_list, 4)

marks = {
    "◎": m1,
    "○": m2,
    "▲": m3,
    "△": m4,
    "×": m5
}

# ----------------------------
# 資金
# ----------------------------

st.sidebar.header("⑤ 資金")

budget = st.sidebar.number_input("予算", value=5000)
unit = st.sidebar.number_input("1点金額", value=100)

# ----------------------------
# 解析
# ----------------------------

def analyze_market(w, qr, ex, tr, tf, sent):

    score = 0

    if w >= 2:
        score += 1

    if qr >= 7:
        score += 1

    if ex >= 15:
        score += 1

    if tr >= 15:
        score += 1

    if tf >= 30:
        score += 1

    if sent == "絶賛（死角なし）":
        score += 1

    if score == 0:
        return "鉄板", "本命信頼"

    elif score <= 2:
        return "標準", "平均レース"

    elif score <= 4:
        return "波乱", "本命危険"

    else:
        return "崩壊", "人気崩壊"


status, comment = analyze_market(
    w_o, qr_o, ex_o, tr_o, tf_o, sentiment
)

distortion = (
    (qr_o / w_o)
    + (ex_o / qr_o)
    + (tr_o / ex_o)
    + (tf_o / tr_o)
)

st.subheader("AI解析")

col1, col2 = st.columns(2)

with col1:
    st.metric("レース判定", status)
    st.metric("オッズ歪み", round(distortion, 2))

with col2:
    st.info(comment)

# ----------------------------
# 買い目
# ----------------------------

if st.button("買い目生成"):

    honmei = marks["◎"]

    ana = [
        marks["○"],
        marks["▲"],
        marks["△"],
        marks["×"]
    ]

    marked = set(marks.values())

    unmarked = [
        h for h in h_list
        if h not in marked
    ]

    g_bd = [
        marks["△"],
        marks["×"]
    ] + unmarked

    A = list(itertools.combinations(ana, 3))

    B = [
        tuple(sorted((honmei, p[0], p[1])))
        for p in itertools.combinations(g_bd, 2)
    ]

    C = list(itertools.combinations(ana, 2))

    D = [(honmei, x) for x in g_bd]

    total = len(A) + len(B) + len(C) + len(D)

    st.subheader("買い目")

    c1, c2 = st.columns(2)

    with c1:

        st.write("3連複BOX")
        st.code("\n".join([f"{a}-{b}-{c}" for a,b,c in A]))

        st.write("馬連BOX")
        st.code("\n".join([f"{a}-{b}" for a,b in C]))

    with c2:

        st.write("3連複軸")
        st.code("\n".join([f"{a}-{b}-{c}" for a,b,c in B]))

        st.write("馬連軸")
        st.code("\n".join([f"{a}-{b}" for a,b in D]))

    invest = total * unit

    st.subheader("投資")

    st.write("点数", total)
    st.write("投資額", invest)

    if invest > budget:
        st.error("予算オーバー")
    else:
        st.success("予算内")

# ----------------------------
# 印一覧
# ----------------------------

st.divider()

df = pd.DataFrame({
    "印": list(marks.keys()),
    "馬番": list(marks.values())
})

st.subheader("印一覧")

st.table(df)
