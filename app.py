from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

if __name__ == "__main__":

    host = os.getenv("FLASK_BIND_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 8080))
    app.run(host=host, port=port, threaded=True)