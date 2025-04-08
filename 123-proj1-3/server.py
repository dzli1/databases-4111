from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Database URI
DATABASEURI = "postgresql://dl3664:815578@34.148.223.31:5432/proj1part2"

# Connect to the database
engine = create_engine(DATABASEURI)
conn = engine.connect()

# Secret key for flash messages
app.secret_key = 'your_secret_key'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        genre = request.form.get("genre")

        query = """
        SELECT s.song_id, s.title, a.name as artist_name, g.name as genre_name, 
        s.duration, s.release_date, s.number_of_streams, al.title as album_name
        FROM song s
        JOIN artist a on s.artist_id = a.artist_id
        JOIN genre g ON s.genre_id = g.genre_id
        JOIN album al ON s.album_id = al.album_id
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
            songs = result.fetchall()
            return render_template("search_results.html", songs=songs)

        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("search.html")
playlist_counter = 16
@app.route("/create_playlist", methods=["GET", "POST"])
def create_playlist():
    global playlist_counter
    if request.method == "POST":
        user_id = request.form.get("user_id")
        title = request.form.get("title")
        creator = request.form.get("creator")
        
        new_playlist_id = playlist_counter
        playlist_counter += 1
        
        insert_query = """
        INSERT INTO playlists (playlist_id, user_id, title, creator, number_of_songs)
        VALUES (:playlist_id, :user_id, :title, :creator, :number_of_songs)
        """

        params = {
            "playlist_id": new_playlist_id,
            "user_id": int(user_id),
            "title": title,
            "creator": creator,
            "number_of_songs": 0
        }
        
        try:
            conn.execute(text(insert_query), params)
            # query = text("SELECT * FROM playlists")
            # result = conn.execute(query)
            # rows = result.fetchall()
            # for row in rows:
            #     print(row)


        except Exception as e:
            #print("Error during insertion:", e)
            return render_template("index.html")
        return render_template("playlist_created.html", playlist_id=new_playlist_id)
    user_id = request.args.get("user_id", "")
    return render_template("create_playlist.html", user_id=user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")

        check_query = """
        SELECT 1
        FROM song_recommendation
        WHERE user_id = :user_id
        LIMIT 1
        """

        try:
            result = conn.execute(text(check_query), {"user_id": user_id})
            user_exists = result.fetchone()

            if not user_exists:
                return render_template("user_not_found.html")
            
            query = """
            SELECT s.song_id, s.title, a.name as artist_name, g.name as genre_name, 
                   s.duration, s.release_date, sr.recommendation_score
            FROM song_recommendation sr
            JOIN song s ON sr.song_id = s.song_id
            JOIN artist a ON s.artist_id = a.artist_id
            JOIN genre g ON s.genre_id = g.genre_id
            WHERE sr.user_id = :user_id
            ORDER BY sr.recommendation_score DESC
            LIMIT 1
            """

            params = {"user_id": user_id}
            result = conn.execute(text(query), params)
            recommended_song = result.fetchone()

            if recommended_song:
                return render_template("recommended_song.html", song=recommended_song)
            else:
                return f"No recommendations found for user {user_id}"

        except Exception as e:
            return f"An error occurred: {e}"
    return render_template("login.html")

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

