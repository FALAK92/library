import streamlit as st
import pandas as pd

# Sample Data (In-memory)
if "books" not in st.session_state:
    st.session_state["books"] = pd.DataFrame(
        columns=["ID", "Title", "Author", "Status"]
    )

# App Title
st.title("📚 Library Management System")

# Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Add Book", "View Books", "Issue Book", "Return Book", "Delete Book"])

# Function to Add a Book
def add_book():
    st.subheader("➕ Add a New Book")
    book_id = st.text_input("Book ID")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    if st.button("Add Book"):
        if book_id and title and author:
            new_book = {"ID": book_id, "Title": title, "Author": author, "Status": "Available"}
            st.session_state["books"] = pd.concat([st.session_state["books"], pd.DataFrame([new_book])], ignore_index=True)
            st.success("Book Added Successfully!")
        else:
            st.error("Please fill all fields.")

# Function to View Books
def view_books():
    st.subheader("📖 Available Books")
    st.da
