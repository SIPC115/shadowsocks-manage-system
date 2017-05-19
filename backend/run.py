from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/index')
def _index():
    return 'hello flask'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
