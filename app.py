import os
import json
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Connect to Redis using the hostname provided by Kubernetes
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
db = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_id = db.incr('task_id_counter')
    task = {"id": task_id, "title": data.get('title'), "status": "pending"}
    
    # Store in Redis as a JSON string
    db.hset('tasks', task_id, json.dumps(task))
    return jsonify({"message": "Task added", "task": task}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Retrieve all tasks from Redis
    raw_tasks = db.hgetall('tasks')
    tasks = [json.loads(task) for task in raw_tasks.values()]
    return jsonify({"tasks": tasks}), 200

@app.route('/health', methods=['GET'])
def health_check():
    try:
        db.ping()
        return jsonify({"state": "healthy", "database": "connected"}), 200
    except redis.ConnectionError:
        return jsonify({"state": "unhealthy", "database": "disconnected"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Test comment
