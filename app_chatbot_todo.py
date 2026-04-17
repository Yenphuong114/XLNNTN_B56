import streamlit as st
import pandas as pd
from datetime import datetime
import json
import re
from collections import Counter


if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    from underthesea import sentiment, word_tokenize
except ImportError:
    sentiment = None
    word_tokenize = None

# ============================================================
# CONSTANTS
# ============================================================
EMOJI_MAP = {"positive": "😊", "negative": "😟", "neutral": "😐"}


# ============================================================
# TODO 1: LOAD STOPWORDS
# ============================================================
def load_stopwords(path: str = "stopwords_vi.txt") -> set[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set([line.strip() for line in f if line.strip()])
    except:
        return set()


STOPWORDS = load_stopwords()


# ============================================================
# TODO 2 + 8 + 13
# ============================================================
@st.cache_resource
def load_model():
    return sentiment, word_tokenize


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # bỏ ký tự đặc biệt
    return text


def analyze_feedback(text: str) -> dict:
    # TODO 13: edge cases
    if not text or len(text.strip()) < 3:
        return {"sentiment": "neutral", "keywords": [], "confidence": 0.0}

    if re.match(r"^[\W_]+$", text):  # emoji only
        return {"sentiment": "neutral", "keywords": [], "confidence": 0.1}

    sentiment_model, tokenizer = load_model()

    clean = clean_text(text)

    # sentiment
    if sentiment_model:
        label = sentiment_model(clean)
        confidence = 0.8  # giả lập vì underthesea không trả score
    else:
        label = "neutral"
        confidence = 0.5

    # keywords
    if tokenizer:
        tokens = tokenizer(clean)
    else:
        tokens = clean.split()

    keywords = [w for w in tokens if w not in STOPWORDS and len(w) > 2]
    keywords = [w for w, _ in Counter(keywords).most_common(10)]

    return {
        "sentiment": label,
        "keywords": keywords,
        "confidence": confidence,
        "text": text,
        "time": datetime.now().isoformat()
    }


# ============================================================
# TODO 3
# ============================================================
def handle_file_upload() -> list[str]:
    uploaded = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        return df.iloc[:, 0].dropna().tolist()

    return []


# ============================================================
# TODO 4
# ============================================================
def export_history(history: list[dict]) -> bytes:
    df = pd.DataFrame(history)
    return df.to_csv(index=False).encode("utf-8")


# ============================================================
# TODO 5
# ============================================================
def render_wordcloud(keywords: list[str]):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    if not keywords:
        return

    wc = WordCloud(width=800, height=400).generate(" ".join(keywords))

    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)


# ============================================================
# TODO 6
# ============================================================
def render_sentiment_timeline(history: list[dict]):
    if not history:
        return

    df = pd.DataFrame(history)
    df["time"] = pd.to_datetime(df["time"])

    sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
    df["score"] = df["sentiment"].map(sentiment_map)

    st.line_chart(df.set_index("time")["score"])


# ============================================================
# TODO 5 + 12
# ============================================================
def render_sidebar_stats(history: list[dict]):
    st.subheader("📊 Thống kê")

    if not history:
        st.write("Chưa có dữ liệu")
        return

    df = pd.DataFrame(history)

    st.write(df["sentiment"].value_counts())

    all_keywords = sum(df["keywords"].tolist(), [])
    render_wordcloud(all_keywords)

    render_sentiment_timeline(history)


# ============================================================
# TODO 7 + 11
# ============================================================
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "history" not in st.session_state:
        st.session_state.history = load_history()


def save_history(history, path="history.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False)


def load_history(path="history.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def delete_feedback(index: int):
    if index < len(st.session_state.history):
        st.session_state.history.pop(index)


# ============================================================
# TODO 9
# ============================================================
def detect_language(text: str) -> str:
    if re.search(r"[àáảãạăâđêôơư]", text.lower()):
        return "vi"
    return "en"


# ============================================================
# TODO 10
# ============================================================
def render_help_page():
    st.title("📘 Hướng dẫn sử dụng")
    st.write("""
    - Nhập phản hồi → chatbot phân tích cảm xúc
    - Upload file CSV để phân tích hàng loạt
    - Xem thống kê bên sidebar
    """)


# ============================================================
# MAIN
# ============================================================
def main():
    st.set_page_config(page_title="Chatbot", layout="wide")

    init_session_state()

    with st.sidebar:
        render_sidebar_stats(st.session_state.history)

        uploaded_texts = handle_file_upload()
        for text in uploaded_texts:
            result = analyze_feedback(text)
            st.session_state.history.append(result)

        if st.button("Export CSV"):
            csv = export_history(st.session_state.history)
            st.download_button("Download", csv, "history.csv")

    st.title("🤖 Chatbot Phân tích phản hồi")

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                if st.button(f"Xóa #{i}"):
                    delete_feedback(i)

    if prompt := st.chat_input("Nhập phản hồi..."):
        lang = detect_language(prompt)

        lines = [l.strip() for l in prompt.splitlines() if l.strip()]

        for line in lines:
            result = analyze_feedback(line)

            st.session_state.history.append(result)

            response = f"""
            **Cảm xúc:** {EMOJI_MAP[result['sentiment']]} {result['sentiment']}
            **Confidence:** {result['confidence']:.2f}
            **Keywords:** {", ".join(result['keywords'])}
            """

            st.session_state.messages.append({"role": "user", "content": line})
            st.session_state.messages.append({"role": "assistant", "content": response})

        save_history(st.session_state.history)
        st.rerun()


if __name__ == "__main__":
    main()