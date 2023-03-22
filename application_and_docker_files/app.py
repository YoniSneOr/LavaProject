from flask import Flask, jsonify

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
    except KeyError:
        return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=5000)