import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Index counter for the servers
server_index = 1

@app.route('/')
def hello():
    global server_index
    server_name = f"server {server_index}"
    server_index += 1
    return f'Hello, you are currently working with {server_name}'

@app.route('/book/<isbn>')
def book_info(isbn):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=:isbn%{isbn}"
        response = requests.get(url, verify=False)
        response.raise_for_status()
        book_info = response.json()
        return jsonify(book_info)
    except requests.exceptions.HTTPError as e:
        # Log failed requests to a local file
        with open('failed_requests.log', 'a') as f:
            f.write(f"{isbn}: {str(e)}\n")
        return f"Error: {str(e)}", 404

@app.route('/cover_image/<isbn>')
def cover_image(isbn):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=:isbn%{isbn}"
        response = requests.get(url, verify=False)
        response.raise_for_status()
        book_info = response.json()
        # Get the cover image URL from the book data
        cover_image_url = book_info['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        if cover_image_url:
            return f"""
            <html>
            <body>
            <h1>{book_info['items'][0]['volumeInfo']['title']}</h1>
            <img src="{cover_image_url}">
            </body>
            </html>
            """
        else:
            return "No cover image available"
    except requests.exceptions.HTTPError as e:
        # Log failed requests to a local file
        with open('failed_requests.log', 'a') as f:
            f.write(f"{isbn}: {str(e)}\n")
        return f"Error: {str(e)}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
