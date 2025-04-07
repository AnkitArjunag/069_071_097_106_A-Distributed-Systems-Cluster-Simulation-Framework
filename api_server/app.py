from flask import Flask, request, jsonify
from node_manager import add_node, list_nodes, delete_node
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "API Server is running! Available endpoints: /add_node, /list_nodes, /delete_node"

@app.route('/add_node', methods=['POST'])
def add_node_api():
    data = request.get_json()
    cpu_cores = data.get('cpu_cores', 1)
    
    node = add_node(cpu_cores)

    # Launch Docker container simulating the node
    subprocess.Popen([
        "docker", "run", "-d",
        "--name", f"node_{node['id'][:8]}",
        "--env", f"NODE_ID={node['id']}",
        "--env", f"API_SERVER_URL=http://host.docker.internal:5000",
        "node-sim"
    ])

    return jsonify({'message': 'Node added', 'node_id': node['id']}), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes_api():
    return jsonify(list_nodes())

@app.route('/delete_node', methods=['POST'])
def delete_node_api():
    data = request.get_json()
    node_id = data.get('id')
    delete_node(node_id)
    return jsonify({'message': f'Node {node_id} deleted'})

if __name__ == '__main__':
    app.run(debug=True)
