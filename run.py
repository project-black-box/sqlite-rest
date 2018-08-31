import os
import sqlite3
from flask import Flask, jsonify
from sqliterest.db.schema import query

#os.environ["FLASK_ENV"]="development"
#os.environ["FLASK_DEBUG"]=1

app = Flask(__name__)

def get_primary_key(conn, table):
    c = conn.cursor()
    rs = c.execute('pragma table_info({})'.format(table)).fetchall()
    # the 6th column from the query above is pk (boolean)
    pk = list(filter(lambda x: x[5] == 1, rs))
    # don't care for compound primary keys yet,
    # so I expect an array (length 1) with a tuple from the query result.
    # the primary key name is the 2nd column.
    return pk[0][1]

def get_foreign_keys(conn, table):
    c = conn.cursor()
    # this is definitely vurnerable to Robert'); DROP TABLE students; --
    rs = c.execute('pragma foreign_key_list({})'.format(table)).fetchall()
    return list(map(lambda x: {"table": x[2], "foreign_key": x[4]}, rs))

def get_select_statement(conn, table):
    primary_key = get_primary_key(conn, table)
    # oh, yes, little bobby tables, we call him.
    return 'select * from {tbl} where {pk} = ?'.format(pk=primary_key, tbl=table)

@app.route('/', methods=['GET'])
def get_tables():
    conn = sqlite3.connect("temp.db")
    c = conn.cursor()
    sql = 'SELECT name FROM sqlite_master WHERE type="table"'
    rs = c.execute(sql)
    result = {"data": rs.fetchall(), "error": {}}
    conn.close()
    return jsonify(result)

@app.route('/<table>', methods=['GET'])
def get_all(table):
    conn = sqlite3.connect("temp.db")
    c = conn.cursor()
    sql = 'select * from {}'.format(table)
    rs = c.execute(sql)
    result = {"data": rs.fetchall(), "error": {}, "links": get_foreign_keys(conn, table)}
    conn.close()
    return jsonify(result)

@app.route('/<table>/<id>', methods=['GET'])
def get_join(table, id):
    conn = sqlite3.connect("temp.db")
    c = conn.cursor()
    sql = get_select_statement(conn, table)
    rs = c.execute(sql, id)
    result = {"data": rs.fetchall(), "error": {}}
    conn.close()
    return jsonify(result)

@app.route('/doc/', defaults={'path': ''})
@app.route('/doc/<path:path>')
def get_dir(path):
    d = lambda x: {"table": x[0], "key": x[1]}
    p = path.split('/')

    if len(p) % 2 == 1:
        p.append(None)

    rest = list(zip(p[::2], p[1::2]))
    rest = [d(x) for x in rest]
    rest = list(reversed(rest))

    return jsonify(rest)

if __name__ == '__main__':
    app.run(debug=True)
