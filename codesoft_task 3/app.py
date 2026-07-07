import streamlit as st
import pandas as pd
import speech_recognition as sr
from PIL import Image
import io

# Page Settings
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

# Load Dataset
movies = pd.read_csv("movies.csv")

st.title("🎬 Movie Recommendation System")
st.write("Get movie recommendations based on your preferences!")

# Sidebar
st.sidebar.header("Filter Movies")

genre = st.sidebar.selectbox(
    "Select Genre",
    sorted(movies["Genre"].unique())
)

language = st.sidebar.selectbox(
    "Select Language",
    sorted(movies["Language"].unique())
)

rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    10.0,
    7.0,
    0.1
)

# Filter Movies
filtered = movies[
    (movies["Genre"] == genre) &
    (movies["Language"] == language) &
    (movies["Rating"] >= rating)
]

st.subheader("🎥 Recommended Movies")

if len(filtered) > 0:
    st.dataframe(filtered, use_container_width=True)
else:
    st.warning("No movies found with these filters.")

# Search Movie
st.subheader("🔍 Search Movie")

search = st.text_input("Enter movie name")

if search:
    result = movies[movies["Title"].str.contains(search, case=False, na=False)]

    if len(result) > 0:
        st.dataframe(result, use_container_width=True)
    else:
        st.error("Movie not found.")

# Voice Search Feature
st.subheader("🎤 Voice Search")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎙️ Start Voice Search"):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening... Speak now!")
                audio = recognizer.listen(source, timeout=10)
            
            voice_text = recognizer.recognize_google(audio)
            st.success(f"You said: {voice_text}")
            
            voice_result = movies[movies["Title"].str.contains(voice_text, case=False, na=False)]
            
            if len(voice_result) > 0:
                st.dataframe(voice_result, use_container_width=True)
            else:
                st.warning(f"No movies found matching '{voice_text}'")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Microphone not available or error occurred: {e}")

# Image Upload & Rating Feature
st.subheader("📸 Upload Movie Poster for Rating")

with col2:
    uploaded_file = st.file_uploader("Upload a movie poster or image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Try to extract title from filename
        filename = uploaded_file.name.split('.')[0].replace('_', ' ').replace('-', ' ')
        
        # Search for movies matching the filename
        image_result = movies[movies["Title"].str.contains(filename, case=False, na=False)]
        
        if len(image_result) > 0:
            st.success("Movie found based on image!")
            st.dataframe(image_result[["Title", "Genre", "Language", "Rating"]], use_container_width=True)
            
            # Display rating prominently
            for idx, row in image_result.iterrows():
                st.metric("Movie Rating", f"⭐ {row['Rating']}/10")
        else:
            st.warning(f"No movies found. Try uploading with a filename like 'Avengers.jpg' or 'John Wick.jpg'")
            st.info(f"Available movies: {', '.join(movies['Title'].unique()[:10])}...")