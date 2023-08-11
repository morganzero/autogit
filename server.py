import subprocess
import logging
from flask import Flask, send_from_directory, send_file
from flask_talisman import Talisman

app = Flask(__name__, static_folder='assets')
csp = {
    'default-src': "'self'",
    'style-src': "'self' 'unsafe-inline'",
    'img-src': "'self' data:",
}
Talisman(app, content_security_policy=csp)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        logs = fetch_logs()
        return logs
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        return "Error fetching logs.", 500

@app.route('/assets/favicon.ico')
def favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
