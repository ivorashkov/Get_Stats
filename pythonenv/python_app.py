import json
import time
import os
import psutil
import socket
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_stats():
    try:
        stats = {
            "PID": os.getpid(),
            "Hostname": socket.gethostname(),
            "Memory_Usage": psutil.virtual_memory().percent,
            "CPU_Usage": psutil.cpu_percent(interval=None),  # Avoid 1s delay
            "Disk_Usage": psutil.disk_usage('/').percent,
            "Uptime": time.time() - psutil.boot_time(),  # System uptime in seconds
            "Network": psutil.net_io_counters()._asdict()
        }
        
        # Read /proc/stat safely
        try:
            with open("/proc/stat", "r") as file:
                stats["Proc_Stat"] = file.read()
        except FileNotFoundError:
            stats["Proc_Stat"] = "N/A"

        return stats
    except Exception as e:
        return {"error": str(e)}

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(get_system_stats())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, threaded=True)