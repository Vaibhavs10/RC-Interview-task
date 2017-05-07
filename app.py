from flask import Flask, jsonify, request
import networkx as nx
import pandas as pd
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(host="localhost", dbname="testpython",
                        user="vaibhavs10", password="")

x = {}
x['relations'] = [(1, 2), (2, 3), (3, 4)]
x['values'] = [(1, "22/11/2014"), (2, "30/02/2016"),
               (3, "12/04/1993"), (4, "10/11/1995")]


@app.route('/shortest_path')
def shortest_path():
    source = request.args.get('source')
    target = request.args.get('target')
    c = conn.cursor()
    c.execute("SELECT * FROM employees;")
    data = c.fetchall()
    G = nx.Graph()
    G.add_edges_from(data)
    path = nx.shortest_path(G, source=source, target=target)
    return jsonify({'data': path})


@app.route('/get_sub_tree')
def sub_tree():
    node = request.args.get('node')
    c = conn.cursor()
    c.execute("WITH RECURSIVE traverse AS (SELECT employee_id FROM employees WHERE dependent_id = %s UNION ALL SELECT employees.employee_id FROM employees INNER JOIN traverse ON employees.dependent_id = traverse.employee_id) SELECT employee_id FROM traverse;", (node,))
    data = c.fetchall()
    c.close()
    return jsonify({'data': data})


@app.route('/get_edges')
def edges():
    node = request.args.get('node')
    c = conn.cursor()
    c.execute("SELECT * FROM employees;")
    data = c.fetchall()
    G = nx.Graph()
    G.add_edges_from(data)
    edge = nx.edges(G, node)
    return jsonify({'data': edge})


@app.route('/get_tree')
def get_tree():
    c = conn.cursor()
    c.execute("WITH RECURSIVE traverse(employee_id, depth) AS ( SELECT employee_id, 1 FROM employees WHERE dependent_id IS NULL UNION ALL SELECT employees.employee_id, traverse.depth + 1 FROM employees INNER JOIN traverse ON employees.dependent_id = traverse.employee_id) SELECT employee_id FROM traverse ORDER BY depth DESC;")
    data = c.fetchall()
    c.close()
    return jsonify({'data': data})


@app.route('/parse_JSON_dump')
def JSON_dump():
    c = conn.cursor()
    for relation in x['relations']:
        c.execute("INSERT INTO employees VALUES %s", (relation,))
    for value in x['values']:
        c.execute("INSERT INTO employee_detail VALUES %s", (value,))
    c.close()
    return jsonify({"data": "Done!"})

if __name__ == "__main__":
    app.run(debug=True)
