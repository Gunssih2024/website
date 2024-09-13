from flask import Flask
from database_manager import DbManager

app = Flask(__name__)

dbm = DbManager("fpgas.json", "gunshots.json")

@app.route("/")
def index():
    return "index"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
