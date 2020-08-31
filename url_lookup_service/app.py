from flask import Flask, jsonify, request
from utils.virustotal import get_url_scan_report, post_url_scan

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({"text": "Hello World!"}), 200


@app.route('/urlinfo/1/<path:route>', methods=['GET'])
def url_lookup(route):

    def _reconstruct_url():
        """Add proper query back in since flask strips it"""
        if request.query_string:
            fixed_url = route + "?" + request.query_string.decode('utf-8')
            return fixed_url
        else:
            return route

    url = _reconstruct_url()
    scan_id, _ = post_url_scan(url)
    report, status_code = get_url_scan_report(scan_id)

    return jsonify({
        "lookup_url": url,
        "safe": report['safe'],
        "details": report['details'],
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
