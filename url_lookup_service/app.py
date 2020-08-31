from flask import Flask, jsonify, request

import mysql.connector
import json
import os
from dotenv import load_dotenv
from utils.vt_utils import get_url_scan_report, post_url_scan
from utils.url_utils import is_url_reachable, is_url_valid

load_dotenv()
app = Flask(__name__)

insert_query = """
INSERT INTO lookup (url, safe, details)
VALUES ('%s', %s, '%s')
"""

get_url_query = """
SELECT * FROM lookup WHERE url="%s"
"""


@app.route('/', methods=['GET'])
def root():
    return jsonify({"text": "Hello World!"}), 200


@app.route('/urlinfo/1/<path:route>', methods=['GET'])
def url_lookup(route):

    config = {
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASS"),
        'host': 'db',
        'port': '3306',
        'database': 'urllookupservice'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    def _reconstruct_url():
        """Add proper query back in since flask strips it"""
        if request.query_string:
            fixed_url = route + "?" + request.query_string.decode('utf-8')
            return fixed_url
        else:
            return route

    url = _reconstruct_url()

    if not is_url_valid(url):
        return jsonify({"reason": "url invalid"}), 400
    if not is_url_reachable(url):
        return jsonify({"reason": "url unreachable"}), 400

    cursor.execute(get_url_query % url)

    data = cursor.fetchone()

    app.logger.info("Retrieved data: %s" % data)

    if data is not None:
        return jsonify({
            "lookup_url": data['url'],
            "safe": True if data['safe'] == 1 else False,
            "details": data['details']
        })

    scan_id, resp_code = post_url_scan(url)

    if resp_code != 200:
        return server_error(resp_code)

    report, resp_code = get_url_scan_report(scan_id)

    if resp_code != 200:
        return server_error(resp_code)

    app.logger.info("Report dump: %s" % str(report))

    cursor.execute(insert_query % (url, "TRUE" if report['safe'] else "FALSE", json.dumps(report['details'])))

    connection.commit()

    cursor.close()

    return jsonify({
        "lookup_url": url,
        "safe": report['safe'],
        "details": report['details'],
    })


def server_error(resp_code):
    return jsonify({"reason": "server error, got %s from internal apis"
                              % resp_code
                    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
