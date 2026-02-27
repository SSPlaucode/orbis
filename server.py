"""
ORBIS - Satellite Tracker Backend
Simple Flask proxy to bypass CORS restrictions when fetching TLE data from Celestrak.

Usage:
    pip install flask flask-cors requests
    python server.py

Then open http://localhost:5000 in your browser.
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)

CELESTRAK_GROUPS = {
    'stations': 'https://celestrak.org/pub/TLE/group/stations.txt',
    'active':   'https://celestrak.org/pub/TLE/group/active.txt',
    'starlink': 'https://celestrak.org/pub/TLE/group/starlink.txt',
    'weather':  'https://celestrak.org/pub/TLE/group/weather.txt',
    'debris':   'https://celestrak.org/pub/TLE/group/1999-025.txt',
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tle/<group>')
def get_tle(group):
    if group not in CELESTRAK_GROUPS:
        return jsonify({'error': 'Unknown group'}), 400
    try:
        url = CELESTRAK_GROUPS[group]
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text, 200, {'Content-Type': 'text/plain'}
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 502

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'groups': list(CELESTRAK_GROUPS.keys())})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🛰  ORBIS backend running at http://localhost:{port}")
    print(f"   Open http://localhost:{port} in your browser\n")
    app.run(debug=True, port=port)
