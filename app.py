from flask import Flask
import threading
import time
import os
import sys

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

def self_destruct():
    time.sleep(180)  # wait 3 minutes
    print("💥 Simulating fatal error...")
    os._exit(1)      # forcefully terminate the process

if __name__ == "__main__":
    threading.Thread(target=self_destruct, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
