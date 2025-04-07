import uuid
from datetime import datetime

# Simple in-memory storage
nodes = {}

def register_node(cpu_cores):
    node_id = str(uuid.uuid4())
    nodes[node_id] = {
        "id": node_id,
        "cpu_cores": cpu_cores,
        "pods": [],
        "last_heartbeat": datetime.now(),
        "status": "Healthy"
    }
    return node_id

def get_all_nodes():
    return nodes
