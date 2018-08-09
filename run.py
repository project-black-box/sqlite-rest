from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/bla')
def bla():
    return "Hello bla!"

if __name__ == '__main__':
    app.run()
