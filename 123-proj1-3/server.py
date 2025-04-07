"""

Flask backend -> sql achemy -> database -> to jinja


DATABASEURI

launch on server

http://<your_server_ip>:8111/
"""

from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)


#TODO
DATABASEURI = "postgresql://dl3664:815578@34.148.223.31:5432/proj1part2"


engine = create_engine(DATABASEURI)
conn = engine.connect()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Get the search term from the form
    title = request.form.get("title")
    artist = request.form.get("artist")
    genre = request.form.get("genre")

    query = """
    SELECT s.song_id, s.title, a.name as artist_name, g.name as genre_name
    FROM song s
    JOIN artist a on s.artist_id = a.artist_id
    JOIN genre g ON s.genre_id = g.genre_id
    WHERE s.title LIKE :title
    AND a.name LIKE :artist
    AND g.name LIKE :genre
    """

    params = {
        "title": f"%{title}%" if title else "%",
        "artist": f"%{artist}%" if artist else "%",
        "genre": f"%{genre}%" if genre else "%",
    }

    try:
        result = conn.execute(text(query), params)
        songs = result.fetchall()  # Get all results
        return render_template("search_results.html", songs=songs)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/test")
def test():
    try:
        result = conn.execute(text("SELECT 1"))
        record = result.fetchone()
        return f"Test query successful. Result: {record[0]}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8111, debug=True)





