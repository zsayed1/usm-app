import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    #  Optional: Show version if provided
    version = os.getenv("APP_VERSION", "unknown")
    return f"Hello, World from ECR + GitHub Actions! (Version: {version})"

if __name__ == "__main__":
    #  Read host and port from environment variables, with safe defaults
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", 8080))

    #  Run Flask using env-provided values (overridden in container / CI/CD)
    app.run(host=host, port=port)
