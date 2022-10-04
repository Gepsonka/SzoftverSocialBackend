from flask import Flask, jsonify



app = Flask(__name__)


@app.route('/')
def geetings():
    return jsonify({'greeting': "Hi there!"})


if __name__=='__main__':
    app.run()