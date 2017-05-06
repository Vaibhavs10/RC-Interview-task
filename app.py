from flask import Flask, render_template, jsonify, request
import networkx as nx
import pandas as pd
import psycopg2

df = pd.DataFrame({'name': ['A', 'B', 'C', 'D', 'E'],
                   'manager': ['Z', 'Z', 'Z', 'X', None],
                   'join_date': ['10/11/1995', '10/11/1996', '10/11/1997', '10/11/1998', '10/11/1999']})

G = nx.from_pandas_dataframe(df, 'name', 'manager', 'join_date')

app = Flask(__name__)


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
