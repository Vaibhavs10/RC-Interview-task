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
    data = nx.shortest_path(G, source=source, target=target)
    return jsonify({'data': data})


@app.route('/get_sub_tree')
def sub_tree():
    node = request.args.get('node')
    data = G[node]
    return jsonify({'data': data})


@app.route('/get_edges')
def edges():
    node = request.args.get('node')
    data = nx.edges(G, node)
    return jsonify({'data': data})


@app.route('/bulk_data_load')
def bulk_data_load():
    data = pd.read_csv('test.csv')
    source = request.args.get('source')
    G = nx.from_pandas_dataframe(data, source, )


if __name__ == "__main__":
    app.run(debug=True)
