from flask import Flask, render_template, jsonify, request
import networkx as nx
import pandas as pd
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(host="localhost", dbname="testpython",
                        user="vaibhavs10", password="")


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


if __name__ == "__main__":
    app.run(debug=True)
