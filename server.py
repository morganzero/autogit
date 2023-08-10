import subprocess
import os
from flask import Flask, send_file, jsonify

app = Flask(__name__)

def fetch_logs():
    try:
        result = subprocess.check_output(['/app/autogit.sh'])
        logs = result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logs = f"Error running autogit.sh: {e}"
    
    print(logs)  # Log the result to see if logs are being fetched correctly.
    return logs

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/logs')
def get_logs():
    logs = fetch_logs()
    return logs

@app.route('/background_image_url')
def background_image_url():
    return jsonify(url=os.environ.get("BACKGROUND_IMAGE_URL", ""))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
