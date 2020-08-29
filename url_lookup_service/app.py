from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({"text": "Hello World!"}), 200


@app.route('/urlinfo/1/<hostname_port>/<path_query>', methods=['GET'])
def url_lookup(hostname_port, path_query):
    return jsonify({"hostname_port": hostname_port,
                    "path_query": path_query})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
