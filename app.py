import streamlit as st
import json
import os
import pandas as pd
from PIL import Image

# Set Page Config with a gradient background using custom CSS
st.set_page_config(page_title="📚 Animated Library Manager", layout="wide")
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background: transparent;
        }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #fff;
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='title'>📚 Animated Library Manager</h1>", unsafe_allow_html=True)

# Library Data File
LIBRARY_FILE = "library.json"

if "library" not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            st.session_state.library = json.load(file)
    else:
        st.session_state.library = []

def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(st.session_state.library, file)

def add_book(title, author, year, genre, read_status, rating, cover_image):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "rating": rating,
        "cover_image": cover_image,
    }
    st.session_state.library.append(book)
    save_library()
    st.success("✨ Book added successfully!")

def display_books(books):
    if not books:
        st.write("No books found.")
    else:
        cols = st.columns(3)
        for i, book in enumerate(books):
            with cols[i % 3]:
                st.image(book.get("cover_image", "https://via.placeholder.com/150"), width=150)
                st.write(f"**{book['title']}**")
                st.write(f"by {book['author']} ({book['year']})")
                st.write(f"Genre: {book['genre']}")
                st.write(f"Rating: {'⭐' * book['rating']}")
                st.write(f"Status: {'✔ Read' if book['read_status'] else '❌ Unread'}")

st.sidebar.header("Menu")
menu_option = st.sidebar.radio(
    "Choose an option:",
    ["Add a Book", "Display All Books"]
)

if menu_option == "Add a Book":
    st.header("📖 Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    rating = st.slider("Rating (1-5 stars)", 1, 5)
    cover_image = st.text_input("Cover Image URL (optional)", "https://via.placeholder.com/150")
    if st.button("Add Book"):
        if title and author and genre:
            add_book(title, author, year, genre, read_status, rating, cover_image)
        else:
            st.error("Please fill in all fields.")

elif menu_option == "Display All Books":
    st.header("📚 Your Library")
    display_books(st.session_state.library)

st.markdown("---")
st.markdown("**Built with ❤️ by Falak Naaz**")
