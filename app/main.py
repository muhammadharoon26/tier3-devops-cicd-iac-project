from flask import Flask, Response
from prometheus_client import generate_latest
from .metrics import request_count, request_latency

app = Flask(__name__)


@app.route("/")
def hello_world():
    request_count.inc()
    return "Hello, DevOps World!"


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
