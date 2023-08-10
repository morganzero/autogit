import subprocess
from flask import Flask, send_file

app = Flask(__name__)

def fetch_logs():
    try:
        result = subprocess.check_output(['/app/auto-git.sh'])
        logs = result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logs = f"Error running auto-git.sh: {e}"
    return logs

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/logs')
def get_logs():
    logs = fetch_logs()
    return logs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
