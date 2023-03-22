from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Index counter for server
server_index = 1

# Book data dictionary
books = {
    "1234567890": {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "year": 1979
    },
    "0987654321": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949
    }
}

@app.route("/")
def hello():
    global server_index
    message = f"Hello, you are currently working with server {server_index}"
    server_index += 1
    return message

@app.route("/book/<isbn>")
def book(isbn):
    try:
        book = books[isbn]
        return jsonify(book)
    except  Exception as e:
        with open("error.log", "a") as f:
            f.write(f"the book search for  ISDN {str(e)}  does not exists.\n")
        return jsonify({"error": "Book not found. Please input a valid ISDN number"}), 404
    
@app.route("/cover_image")
def cover_image():
    isbn = request.args.get("isbn")
    try:
        # fetch book metadata and cover image using ISBN
        book_metadata = {
            "title": "Sample Book",
            "author": "John Doe",
            "publisher": "Random House",
            "isbn": isbn
        }
        return f"""
            <html>
                <head><title>{book_metadata['title']}</title></head>
                <body>
                    <h1>{book_metadata['title']}</h1>
                    <p>Author: {book_metadata['author']}</p>
                    <p>Publisher: {book_metadata['publisher']}</p>
                    <p>ISBN: {book_metadata['isbn']}</p>
                    <img src="https://example.com/cover/{isbn}.jpg" alt="Book cover">
                </body>
            </html>
        """

if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=8000)