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
DATABASEURI = "postgresql://username:password@[ip]]:[port]/[name]"


engine = create_engine(DATABASEURI)
conn = engine.connect()

@app.route("/")
def index():
    return "Welcome to the bare-bones Flask web application!"

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
