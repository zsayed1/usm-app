from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Bind host and port from env vars or use defaults
    host = os.getenv("FLASK_BIND_HOST", "0.0.0.0")  # 0.0.0.0 to listen externally
    port = int(os.getenv("FLASK_PORT", 8080))
    # Enable threaded server for better concurrency
    app.run(host=host, port=port, threaded=True)
