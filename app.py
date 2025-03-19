import streamlit as st
import json
import os
from PIL import Image
from fpdf import FPDF

# Set Page Config with Background Image
st.set_page_config(page_title="📚 Animated Library Manager", layout="wide")

# Custom CSS for Background Image & Styling
st.markdown(
    """
    <style>
        .stApp {
            background: url('https://source.unsplash.com/1600x900/?library,books') no-repeat center center fixed;
            background-size: cover;
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

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(st.session_state.library, file)

if "library" not in st.session_state:
    st.session_state.library = load_library()

def add_book(title, author, year, genre, read_status, rating, cover_image):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "rating": rating,
        "cover_image": cover_image or "https://via.placeholder.com/150",
    }
    st.session_state.library.append(book)
    save_library()
    st.success("✨ Book added successfully!")

def delete_book(index):
    del st.session_state.library[index]
    save_library()
    st.success("🗑️ Book deleted successfully!")

def edit_book(index, title, author, year, genre, read_status, rating, cover_image):
    st.session_state.library[index] = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "rating": rating,
        "cover_image": cover_image or "https://via.placeholder.com/150",
    }
    save_library()
    st.success("✏️ Book edited successfully!")

def download_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "📚 Library Books", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for book in st.session_state.library:
        pdf.cell(200, 10, f"📖 {book['title']} - {book['author']} ({book['year']})", ln=True)
        pdf.cell(200, 10, f"   Genre: {book['genre']} | Rating: {'⭐' * book['rating']} | Status: {'✔ Read' if book['read_status'] else '❌ Unread'}", ln=True)
        pdf.ln(5)
    pdf_output = "library_books.pdf"
    pdf.output(pdf_output)
    return pdf_output

st.sidebar.header("📌 Menu")
menu_option = st.sidebar.radio("Choose an option:", ["Add a Book", "Display All Books"])

if menu_option == "Add a Book":
    st.header("📖 Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    rating = st.slider("Rating (1-5 stars)", 1, 5)
    cover_image = st.text_input("Cover Image URL (optional)")
    if st.button("Add Book"):
        if title and author and genre:
            add_book(title, author, year, genre, read_status, rating, cover_image)
        else:
            st.error("Please fill in all fields.")

elif menu_option == "Display All Books":
    st.header("📚 Your Library")
    if not st.session_state.library:
        st.write("No books found.")
    else:
        for i, book in enumerate(st.session_state.library):
            with st.expander(f"📖 {book['title']}"):
                st.image(book.get("cover_image", "https://via.placeholder.com/150"), width=150)
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Rating:** {'⭐' * book['rating']}")
                st.write(f"**Status:** {'✔ Read' if book['read_status'] else '❌ Unread'}")
                if st.button(f"✏️ Edit", key=f"edit_{i}"):
                    edit_book(i, title, author, year, genre, read_status, rating, cover_image)
                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    delete_book(i)
    pdf_file = download_pdf()
    with open(pdf_file, "rb") as file:
        st.download_button("📥 Download Library as PDF", file, file_name=pdf_file)

st.markdown("---")
st.markdown("**Built with ❤️ by Falak Naaz**")
