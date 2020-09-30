"""
Basic Flask application that utilises VirusTotal's API to lookup urls to check if they are safe or not.
It then stores the result of this lookup in a MySQL DB.
"""
import json

from flask import Flask, jsonify, request

from database import Database
from utils.url_utils import is_url_reachable, is_url_valid
from utils.vt_utils import get_url_scan_report, post_url_scan

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({"text": "Hello World!"}), 200


@app.route('/urlinfo/1/<path:route>', methods=['GET'])
def url_lookup(route):
    """

    :param route: path given after 1 includes queries (but stripping ?)
    :return:
    """

    def _reconstruct_url():
        """Add proper query back in since flask strips it"""
        if request.query_string:
            fixed_url = route + "?" + request.query_string.decode('utf-8')
            return fixed_url
        else:
            return route

    database = Database()

    url = _reconstruct_url()

    if not is_url_valid(url):
        return jsonify({"reason": "url invalid"}), 400
    if not is_url_reachable(url):
        return jsonify({"reason": "url unreachable"}), 400

    # check if the url is in the database already (i.e; we've looked it up before)
    data = database.fetch_by_url(url)

    app.logger.info("Retrieved data: %s" % data)

    # return the data found about the url
    if data is not None:
        return jsonify({
            "lookup_url": data['url'],
            "safe": True if data['safe'] == 1 else False,
            "details": json.loads(data['details'])
        })

    # send url off to VT to be scanned
    scan_id, resp_code = post_url_scan(url)

    if resp_code != 200:
        return server_error(resp_code)

    # get result of scan from VT
    report, resp_code = get_url_scan_report(scan_id)

    if resp_code != 200:
        return server_error(resp_code)

    app.logger.info("Report dump: %s" % str(report))

    # push new data about url from VT to db
    database.push_data_from_report(url, report)

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
