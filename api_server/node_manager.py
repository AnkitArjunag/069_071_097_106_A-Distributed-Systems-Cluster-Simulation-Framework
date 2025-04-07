import uuid
import json
import os
import subprocess
from datetime import datetime

DATA_FILE = 'nodes.json'
nodes = {}

# Load nodes into memory at startup
def load_nodes_from_file():
    global nodes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                nodes = json.load(f)
            except json.JSONDecodeError:
                nodes = {}
    else:
        nodes = {}
    return nodes

# Save in-memory nodes to file
def save_nodes_to_file(nodes):
    with open(DATA_FILE, 'w') as f:
        json.dump(nodes, f, indent=4)

# Add a new node
def add_node(cpu_cores):
    global nodes
    node_id = str(uuid.uuid4())
    nodes[node_id] = {
        'id': node_id,
        'cpu_cores': cpu_cores,
        'status': 'Healthy',
        'pods': [],
        'last_heartbeat': datetime.utcnow().isoformat()
    }
    save_nodes_to_file(nodes)
    return nodes[node_id]

# Get all nodes
def list_nodes():
    return list(nodes.values())

# Delete a node
def delete_node(node_id):
    nodes = load_nodes_from_file()
    if node_id in nodes:
        # Stop and remove Docker container
        container_name = f"node_{node_id[:8]}"
        subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Remove from storage
        del nodes[node_id]
        save_nodes_to_file(nodes)

# Load nodes once on module load
load_nodes_from_file()
