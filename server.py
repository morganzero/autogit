import subprocess
from flask import Flask, send_from_directory, send_file

app = Flask(__name__, static_folder='assets')

def fetch_logs():
    try:
        result = subprocess.check_output(['/app/auto-git.sh'])
        logs = result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logs = f"Error running auto-git.sh: {e.output.decode('utf-8')}"
    return logs

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/logs')
def get_logs():
    logs = fetch_logs()
    return logs

@app.route('/assets/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
