from flask import Flask, request, Response, render_template
import requests
import json

app = Flask(__name__)
TARGETS = {}

@app.route("/")
def home():
    return render_template('index.html', targets=TARGETS)

@app.route('/<app>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<app>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(app, path=''):
    target_config = TARGETS.get(app)
    if not target_config:
        return 'Unknown proxy target', 404

    base = target_config['target']
    prefix = f"/{app}"
    url = f"{base}/{path}"

    headers = {
      key: value for key, value in request.headers if key.lower() != 'host'
    }
    headers['X-Script-Name'] = prefix

    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )


    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)

def start_gateway(host='127.0.0.1', port=9999, targets_path=None):
    if targets_path:
        global TARGETS
        with open(targets_path) as f:
            TARGETS = json.load(f)

    app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    start_gateway()
