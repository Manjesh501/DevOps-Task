from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import os

app = Flask(__name__)

# Create metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration', ['method', 'endpoint'])
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
UPTIME = Gauge('uptime_seconds', 'Application uptime')

# Store start time for uptime calculation
START_TIME = time.time()

# Request tracking
@app.before_request
def before_request():
    # Start timer for request duration
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Record request metrics
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    
    # Record request duration if start_time was set
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        REQUEST_DURATION.labels(method=request.method, endpoint=request.endpoint).observe(duration)
    
    return response

@app.route('/metrics')
def metrics():
    # Update system metrics
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process(os.getpid()).memory_info().rss)
    UPTIME.set(time.time() - START_TIME)
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/status')
def status():
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)