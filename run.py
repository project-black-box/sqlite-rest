import os
import sqlite3
from flask import Flask, jsonify
from sqliterest.db.schema import query

#os.environ["FLASK_ENV"]="development"
#os.environ["FLASK_DEBUG"]=1

app = Flask(__name__)

def parse_path(path):
    transform = lambda x: {"name": x[0], "key": x[1]}
    p = path.split('/')

    if len(p) % 2 == 1:
        p.append(None)

    rest = list(zip(p[::2], p[1::2]))
    rest = [transform(x) for x in rest]
    return list(reversed(rest))

@app.route('/doc/', defaults={'path': ''})
@app.route('/doc/<path:path>')
def get_dir(path):
    p = parse_path(path)
    res = query(p)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
