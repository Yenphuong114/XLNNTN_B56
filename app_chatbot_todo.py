# ============================================================
# TODO LIST – app_chatbot.py (Chatbot Phân tích Phản hồi SV)
# ============================================================
#
# TODO 1: Mở rộng danh sách STOPWORDS tiếng Việt (hiện chỉ ~40 từ, nên dùng file ngoài hoặc thư viện chuẩn)
# TODO 2: Thêm caching (@st.cache_resource / @st.cache_data) cho model underthesea để tránh load lại mỗi lần rerun
# TODO 3: Hỗ trợ upload file CSV/Excel phản hồi bên cạnh nhập tay qua chat
# TODO 4: Thêm chức năng xuất lịch sử phân tích ra CSV/Excel (nút download ở sidebar)
# TODO 5: Hiển thị word cloud từ khóa thay vì chỉ bảng top 10
# TODO 6: Thêm biểu đồ xu hướng cảm xúc theo thời gian (timeline) khi có nhiều phản hồi
# TODO 7: Cho phép người dùng chỉnh sửa / xóa từng phản hồi đã gửi trong lịch sử chat
# TODO 8: Thêm confidence score cho kết quả phân tích cảm xúc (nếu model hỗ trợ)
# TODO 9: Hỗ trợ phân tích đa ngôn ngữ (detect ngôn ngữ trước khi chọn pipeline)
# TODO 10: Thêm trang "Hướng dẫn sử dụng" hoặc tooltip giải thích ý nghĩa từng chỉ số
# TODO 11: Persist lịch sử chat vào file/DB để không mất khi reload trang
# TODO 12: Thêm chế độ so sánh: nhập 2 nhóm phản hồi (VD: trước/sau cải tiến) và so sánh kết quả
# TODO 13: Xử lý edge case: phản hồi quá ngắn (1-2 từ), emoji-only, hoặc chứa ký tự đặc biệt
# TODO 14: Thêm unit test cho hàm analyze_feedback và render_analysis
# TODO 15: Tách logic phân tích ra module riêng (analyzer.py) để dễ tái sử dụng và test

# ============================================================
# IMPORTS
# ============================================================
import streamlit as st
import pandas as pd
from datetime import datetime

try:
    from underthesea import sentiment, word_tokenize
except ImportError:
    sentiment = None
    word_tokenize = None


# ============================================================
# CONSTANTS
# ============================================================
STOPWORDS: set[str] = set()  # TODO 1: load từ file ngoài
EMOJI_MAP = {"positive": "😊", "negative": "😟", "neutral": "😐"}


# ============================================================
# HÀM PHÂN TÍCH
# ============================================================
def load_stopwords(path: str = "stopwords_vi.txt") -> set[str]:
    """TODO 1: Đọc stopwords từ file ngoài, trả về set."""
    pass


def analyze_feedback(text: str) -> dict:
    """Phân tích cảm xúc + trích xuất từ khóa từ một phản hồi.
    TODO 2: Thêm caching cho model
    TODO 8: Trả thêm confidence score
    TODO 13: Xử lý edge case (quá ngắn, emoji-only, ký tự đặc biệt)
    """
    pass


def render_analysis(result: dict) -> str:
    """Tạo markdown hiển thị kết quả phân tích trong chat bubble."""
    pass


# ============================================================
# HÀM UPLOAD / EXPORT
# ============================================================
def handle_file_upload() -> list[str]:
    """TODO 3: Đọc file CSV/Excel upload, trả về list phản hồi."""
    pass


def export_history(history: list[dict]) -> bytes:
    """TODO 4: Chuyển lịch sử phân tích thành CSV bytes để download."""
    pass


# ============================================================
# HÀM VISUALIZATION
# ============================================================
def render_wordcloud(keywords: list[str]):
    """TODO 5: Vẽ word cloud từ danh sách từ khóa."""
    pass


def render_sentiment_timeline(history: list[dict]):
    """TODO 6: Vẽ biểu đồ xu hướng cảm xúc theo thời gian."""
    pass


def render_sidebar_stats(history: list[dict]):
    """Hiển thị thống kê tổng hợp trên sidebar (biểu đồ, metric, top từ khóa).
    TODO 5: Tích hợp word cloud
    TODO 12: Thêm chế độ so sánh 2 nhóm
    """
    pass


# ============================================================
# HÀM QUẢN LÝ LỊCH SỬ
# ============================================================
def init_session_state():
    """Khởi tạo session_state: messages, history."""
    pass


def save_history(history: list[dict], path: str = "history.json"):
    """TODO 11: Persist lịch sử ra file JSON/DB."""
    pass


def load_history(path: str = "history.json") -> list[dict]:
    """TODO 11: Load lịch sử từ file JSON/DB."""
    pass


def delete_feedback(index: int):
    """TODO 7: Xóa một phản hồi theo index khỏi history + messages."""
    pass


# ============================================================
# HÀM ĐA NGÔN NGỮ
# ============================================================
def detect_language(text: str) -> str:
    """TODO 9: Detect ngôn ngữ, trả về mã ('vi', 'en', ...)."""
    pass


# ============================================================
# HÀM UI PHỤ
# ============================================================
def render_help_page():
    """TODO 10: Hiển thị trang hướng dẫn sử dụng."""
    pass


# ============================================================
# MAIN
# ============================================================
def main():
    st.set_page_config(page_title="Chatbot Phân tích phản hồi", page_icon="🤖", layout="wide")

    init_session_state()

    # ── Sidebar ──
    with st.sidebar:
        render_sidebar_stats(st.session_state.history)
        # TODO 3: handle_file_upload()
        # TODO 4: nút export_history()

    # ── Main area ──
    st.title("🤖 Chatbot Phân tích Phản hồi Sinh viên")

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập chat
    if prompt := st.chat_input("Nhập phản hồi của bạn tại đây..."):
        # TODO 9: detect_language(prompt) → chọn pipeline
        # Phân tích từng dòng
        lines = [l.strip() for l in prompt.splitlines() if l.strip()]
        # ... gọi analyze_feedback, render_analysis, cập nhật history
        pass


if __name__ == "__main__":
    main()
