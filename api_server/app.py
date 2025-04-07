from flask import Flask, request, jsonify
from node_manager import register_node, get_all_nodes
import subprocess

app = Flask(__name__)

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    cpu_cores = data.get("cpu_cores")
    if not cpu_cores:
        return jsonify({"error": "Missing cpu_cores"}), 400

    # Register the node
    node_id = register_node(cpu_cores)

    # Launch Docker container simulating the node
    subprocess.Popen([
        "docker", "run", "-d",
        "--name", f"node_{node_id[:8]}",
        "--env", f"NODE_ID={node_id}",
        "--env", f"API_SERVER_URL=http://host.docker.internal:5000",
        "node-sim"
    ])

    return jsonify({"message": "Node added", "node_id": node_id}), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(get_all_nodes())

@app.route('/list_nodes', methods=['GET'])
def get_node_list():
    nodes = node_manager.get_all_nodes()
    return jsonify(nodes)


if __name__ == '__main__':
    app.run(debug=True)
