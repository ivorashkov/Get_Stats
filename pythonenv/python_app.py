import json
import time
import os
import psutil
import socket
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_stats():
    stats = {}
    stats["PID"] = os.getpid()
    stats["Hostname"] = socket.gethostname()
    stats["Memory_Usage"] = psutil.virtual_memory().percent
    stats["CPU_Usage"] = psutil.cpu_percent(interval=1)
    
    with open("/proc/stat", "r") as file:
        stats["Proc_Stat"] = file.read()
    
    return stats

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(get_system_stats())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)