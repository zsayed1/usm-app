import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World from ECR + GitHub Actions!"

if __name__ == "__main__":
    # ✅ Use environment variables instead of hardcoding values
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", 8080))

    # Flask will run on localhost by default, unless overridden by env vars
    app.run(host=host, port=port)
