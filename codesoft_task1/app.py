from datetime import datetime
import re

import pandas as pd
import streamlit as st
from pandas.errors import EmptyDataError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="FAQ Chatbot", page_icon=":material/smart_toy:")


@st.cache_data
def load_faq_data() -> pd.DataFrame:
    try:
        data = pd.read_csv("faq_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Question", "Answer"])
    except EmptyDataError:
        return pd.DataFrame(columns=["Question", "Answer"])

    expected_columns = {"Question", "Answer"}
    if not expected_columns.issubset(data.columns):
        return pd.DataFrame(columns=["Question", "Answer"])

    return data.dropna(subset=["Question", "Answer"]).reset_index(drop=True)


def clean_text(text: str) -> str:
    text = text.lower()
    return re.sub(r"[^\w\s]", "", text)


def rule_based_response(text: str) -> str | None:
    text = text.lower().strip()

    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello! Welcome to the FAQ Chatbot. How can I help you today?"
    if "how are you" in text:
        return "I'm doing great. Thanks for asking."
    if "your name" in text:
        return "My name is FAQ Chatbot."
    if "who made you" in text or "creator" in text:
        return "I was developed by Karan Yadav."
    if "time" in text:
        return f"Current time: {datetime.now().strftime('%I:%M %p')}"
    if "date" in text:
        return f"Today's date: {datetime.now().strftime('%d-%m-%Y')}"
    if "thanks" in text or "thank you" in text:
        return "You're welcome."
    if "bye" in text or "goodbye" in text:
        return "Goodbye. Have a great day."
    if "help" in text:
        return (
            "You can ask me about:\n"
            "- Admission\n"
            "- Courses\n"
            "- Fees\n"
            "- Hostel\n"
            "- Placement"
        )

    return None


data = load_faq_data()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("FAQ Chatbot")
st.sidebar.write(f"Total FAQs: {len(data)}")
st.sidebar.write(f"Messages: {len(st.session_state.messages)}")

search = st.sidebar.text_input("Search FAQ")
if search and not data.empty:
    result = data[data["Question"].str.contains(search, case=False, na=False)]
    st.sidebar.dataframe(result, width="stretch")

chat_history = ""
for msg in st.session_state.messages:
    chat_history += f"{msg['role']}: {msg['content']}\n\n"

st.sidebar.download_button(
    "Download chat",
    chat_history,
    file_name="chat_history.txt",
)

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

st.title("FAQ Chatbot")

if data.empty:
    st.warning(
        "faq_data.csv is empty or missing the required Question and Answer columns. "
        "Add FAQ rows to enable similarity-based answers."
    )

questions = data["Question"].reset_index(drop=True) if not data.empty else pd.Series(dtype=str)
answers = data["Answer"].reset_index(drop=True) if not data.empty else pd.Series(dtype=str)
cleaned_questions = [clean_text(question) for question in questions]

vectorizer = None
question_vectors = None
if cleaned_questions:
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(cleaned_questions)

user_input = st.chat_input("Ask your question")
confidence = 0.0

if user_input:
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "time": current_time,
        }
    )

    rule_response = rule_based_response(user_input)

    if rule_response:
        response = rule_response
    elif vectorizer is None or question_vectors is None:
        response = (
            "I do not have FAQ data loaded yet. Please add questions and answers "
            "to faq_data.csv, then ask again."
        )
    else:
        cleaned_input = clean_text(user_input)
        user_vector = vectorizer.transform([cleaned_input])
        similarity = cosine_similarity(user_vector, question_vectors)

        top_indices = similarity.argsort()[0][-3:][::-1]
        similar_questions = [questions.iloc[i] for i in top_indices]

        score = similarity.max()
        index = similarity.argmax()
        confidence = round(score * 100, 2)

        if score < 0.3:
            response = (
                "Sorry, I couldn't understand your question.\n\n"
                "Try asking about:\n"
                "- Admission\n"
                "- Courses\n"
                "- Fees\n"
                "- Hostel\n"
                "- Placement"
            )
        else:
            response = answers.iloc[index]
            response += f"\n\nConfidence score: {confidence}%"
            response += "\n\nRelated questions:\n"
            for question in similar_questions:
                response += f"- {question}\n"

    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "time": current_time,
        }
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "time" in msg:
            st.caption(msg["time"])

if user_input and confidence:
    st.progress(int(confidence))
    st.caption(f"Confidence: {confidence}%")

feedback = st.radio(
    "Was this answer helpful?",
    ["Yes", "No"],
    horizontal=True,
)

if feedback == "Yes":
    st.success("Thanks for your feedback.")
