from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/foo', methods=['GET'])
def foo():
    return jsonify({ 'foo': 'OK' })

@app.route('/api/v1/bar', methods=['GET'])
def bar():
    return jsonify({ 'bar': 'OK' })


if __name__ == '__main__':
    print('Running..')
    app.run(host='0.0.0.0')
