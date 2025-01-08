from prometheus_client import Counter, Histogram

request_count = Counter(
    "app_request_count", "Total number of requests to the web application"
)

request_latency = Histogram("app_request_latency_seconds", "Request latency in seconds")
