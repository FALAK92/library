import streamlit as st
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        year INTEGER
                    )''')
    conn.commit()
    conn.close()

# Add book
def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

# View all books
def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Edit book
def edit_book(book_id, title, author, year):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, book_id))
    conn.commit()
    conn.close()

# Delete book
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Streamlit UI
st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f6d365, #fda085);
        background-attachment: fixed;
    }
    .stApp {
        background: url('https://source.unsplash.com/1600x900/?library,books') no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Library Management System")

menu = ["Add Book", "View Books", "Edit Book", "Delete Book"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("Add New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=1000, max_value=9999, step=1)
    if st.button("Add Book"):
        add_book(title, author, year)
        st.success(f"Book '{title}' added successfully!")

elif choice == "View Books":
    st.subheader("View All Books")
    books = view_books()
    for book in books:
        st.write(f"📖 {book[1]} by {book[2]} ({book[3]})")

elif choice == "Edit Book":
    st.subheader("Edit Book")
    books = view_books()
    book_options = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
    selected_book = st.selectbox("Select a book to edit", list(book_options.keys()))
    if selected_book:
        book_id = book_options[selected_book]
        new_title = st.text_input("New Title", selected_book.split(" by ")[0])
        new_author = st.text_input("New Author", selected_book.split(" by ")[1].split(" (")[0])
        new_year = st.number_input("New Year", min_value=1000, max_value=9999, step=1, value=int(selected_book.split(" (")[1][:-1]))
        if st.button("Update Book"):
            edit_book(book_id, new_title, new_author, new_year)
            st.success("Book updated successfully!")

elif choice == "Delete Book":
    st.subheader("Delete Book")
    books = view_books()
    book_options = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
    selected_book = st.selectbox("Select a book to delete", list(book_options.keys()))
    if selected_book:
        book_id = book_options[selected_book]
        if st.button("Delete Book"):
            delete_book(book_id)
            st.success("Book deleted successfully!")
