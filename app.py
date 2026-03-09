import streamlit as st
import itertools

# 1. 表示設定（ここは変えていません）
st.set_page_config(page_title="LaLaLa式・裏読みAI", layout="wide")
st.title("🏇 LaLaLa式・究極の裏読み解析システム")

# 2. オッズ入力（ここも変えていません）
st.sidebar.header("1. 5大オッズ1番人気")
w_o = st.sidebar.number_input("単勝", value=1.5, step=0.1)
qr_o = st.sidebar.number_input("馬連", value=3.5, step=0.1)
ex_o = st.sidebar.number_input("馬単", value=7.0, step=0.1)
tr_o = st.sidebar.number_input("3連複", value=8.0, step=0.1)
tf_o = st.sidebar.number_input("3連単", value=15.0, step=1.0)

st.sidebar.header("2. 一番人気の評判")
sentiment = st.sidebar.selectbox("記事のトーン", ["絶賛（死角なし）", "普通（一長一短）", "不安（疑問あり）"])

st.sidebar.header("3. 馬番（人気1-10位）")
h_in = st.sidebar.text_input("10頭をカンマ区切りで", "1,2,3,4,5,6,7,8,9,10")
h_list = [h.strip() for h in h_in.split(",")]

st.sidebar.header("4. LaLaLaの直感印")
if len(h_list) >= 5:
    # 修正箇所：内部的な名前を m1, m2... に変更（表示は ◎, ○ のままです）
    m1 = st.sidebar.selectbox("◎ 本命", h_list, index=0)
    m2 = st.sidebar.selectbox("○ 対抗", h_list, index=1)
    m3 = st.sidebar.selectbox("▲ 黒三角", h_list, index=2)
    m4 = st.sidebar.selectbox("△ 白三角", h_list, index=3)
    m5 = st.sidebar.selectbox("× ペケ", h_list, index=4)
    marks = {'◎': m1, '○': m2, '▲': m3, '△': m4, '×': m5}

# 3. 裏読み判定（ここも変えていません）
def analyze_v3(w, qr, ex, tr, tf, sent):
    score = 0
    if w >= 2.0: score += 1
    if qr >= 7.0: score += 1
    if ex >= 15.0: score += 1
    if tr >= 15.0: score += 1
    if tf >= 30.0: score += 1
    if sent == "絶賛（死角なし）" and score >= 1: score += 2
    
    if score == 0: return "【鉄板】信頼度・極高", "本命は堅実。B・Dを厚めに。", "success"
    elif score <= 2: return "【普通】標準的な信頼", "特筆すべき歪みなし。全パターン均等に。", "info"
    elif score <= 4: return "【波乱】裏読み推奨", "一番人気が飛ぶ予兆あり。A・Cをメインに！", "warning"
    else: return "【混沌】崩壊の危機", "市場評価がバラバラ。本命を捨てたBOX(A・C)の好機！", "error"

status, advice, color = analyze_v3(w_o, qr_o, ex_o, tr_o, tf_o, sentiment)

st.subheader("📊 多次元解析・最終判定")
if color == "success": st.success(f"判定：{status}\n\n{advice}")
elif color == "error": st.error(f"判定：{status}\n\n{advice}")
elif color == "warning": st.warning(f"判定：{status}\n\n{advice}")
else: st.info(f"判定：{status}\n\n{advice}")

# 4. 買い目生成（ここもロジックは変えていません）
if st.button("🚀 38点の買い目を生成する"):
    g_ac = sorted([marks['○'], marks['▲'], marks['△'], marks['×']])
    m_vals = set(marks.values())
    unmarked = [h for h in h_list if h not in m_vals]
    g_bd_opp = sorted([marks['△'], marks['×']] + unmarked)
    
    a_b = list(itertools.combinations(g_ac, 3))
    b_b = [tuple(sorted((marks['◎'], p[0], p[1]))) for p in itertools.combinations(g_bd_opp, 2)]
    c_b = list(itertools.combinations(g_ac, 2))
    d_b = [(marks['◎'], opp) for opp in g_bd_opp]

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"A: 3連複BOX ({len(a_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}-{b[2]}" for b in a_b]))
        st.subheader(f"C: 馬連BOX ({len(c_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}" for b in c_b]))
    with c2:
        st.subheader(f"B: 3連複◎軸流し ({len(b_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}-{b[2]}" for b in b_b]))
        st.subheader(f"D: 馬連◎軸流し ({len(d_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}" for b in d_b]))    if qr >= 7.0: score += 1
    if ex >= 15.0: score += 1
    if tr >= 15.0: score += 1
    if tf >= 30.0: score += 1
    if sent == "絶賛（死角なし）" and score >= 1: score += 2
    
    if score == 0: return "【鉄板】信頼度・極高", "本命は堅実。B・Dを厚めに。", "success"
    elif score <= 2: return "【普通】標準的な信頼", "特筆すべき歪みなし。全パターン均等に。", "info"
    elif score <= 4: return "【波乱】裏読み推奨", "一番人気が飛ぶ予兆あり。A・Cをメインに！", "warning"
    else: return "【混沌】崩壊の危機", "市場評価がバラバラ。本命を捨てたBOX(A・C)の好機！", "error"

status, advice, color = analyze_v3(w_o, qr_o, ex_o, tr_o, tf_o, sentiment)

st.subheader("📊 多次元解析・最終判定")
if color == "success": st.success(f"判定：{status}\n\n{advice}")
elif color == "error": st.error(f"判定：{status}\n\n{advice}")
elif color == "warning": st.warning(f"判定：{status}\n\n{advice}")
else: st.info(f"判定：{status}\n\n{advice}")

if st.button("🚀 38点の買い目を生成する"):
    g_ac = sorted([marks['○'], marks['▲'], marks['△'], marks['×']])
    m_vals = set(marks.values())
    unmarked = [h for h in h_list if h not in m_vals]
    g_bd_opp = sorted([marks['△'], marks['×']] + unmarked)
    a_b = list(itertools.combinations(g_ac, 3))
    b_b = [tuple(sorted((marks['◎'], p[0], p[1]))) for p in itertools.combinations(g_bd_opp, 2)]
    c_b = list(itertools.combinations(g_ac, 2))
    d_b = [(marks['◎'], opp) for opp in g_bd_opp]
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"A: 3連複BOX ({len(a_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}-{b[2]}" for b in a_b]))
        st.subheader(f"C: 馬連BOX ({len(c_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}" for b in c_b]))
    with c2:
        st.subheader(f"B: 3連複◎軸流し ({len(b_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}-{b[2]}" for b in b_b]))
        st.subheader(f"D: 馬連◎軸流し ({len(d_b)}点)"); st.code("\n".join([f"{b[0]}-{b[1]}" for b in d_b]))
