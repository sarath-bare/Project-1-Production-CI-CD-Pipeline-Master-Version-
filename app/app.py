from flask import Flask
import socket
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.route("/")
def home():
    return {
        "application": "Production CI/CD Pipeline",
        "version": VERSION,
        "hostname": socket.gethostname(),
        "status": "running"
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/version")
def version():
    return {
        "version": VERSION
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
