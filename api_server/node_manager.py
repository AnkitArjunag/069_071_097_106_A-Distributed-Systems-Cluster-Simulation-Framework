import uuid
import json
import os
import subprocess
from datetime import datetime, timedelta

DATA_FILE = 'nodes.json'
nodes = {}

PODS_FILE = 'pods.json'
pods = {}

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

def load_pods():
    if os.path.exists(PODS_FILE):
        with open(PODS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_pods(pods):
    with open(PODS_FILE, 'w') as f:
        json.dump(pods, f, indent=4)

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
    global nodes
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
    
def check_node_health():
    nodes = load_nodes_from_file()
    pods = load_pods()
    changed = False

    for node_id, node in nodes.items():
        last_beat = datetime.fromisoformat(node['last_heartbeat'])
        if datetime.utcnow() - last_beat > timedelta(seconds=10):
            if node['status'] != 'Unhealthy':
                print(f"Node {node_id} is marked Unhealthy")
                node['status'] = 'Unhealthy'
                changed = True

                # Reschedule all pods from this node
                for pod in node['pods']:
                    pod_id = pod['id']
                    cpu = pod['cpu']

                    # Attempt to reschedule
                    new_node = None
                    for new_node_id, new_node_obj in nodes.items():
                        if new_node_id != node_id and new_node_obj['status'] == 'Healthy':
                            used_cpu = sum(p['cpu'] for p in new_node_obj['pods'])
                            available_cpu = new_node_obj['cpu_cores'] - used_cpu

                            if available_cpu >= cpu:
                                new_node_obj['pods'].append({'id': pod_id, 'cpu': cpu})
                                pods[pod_id]['node_id'] = new_node_id
                                print(f"Pod {pod_id} rescheduled from {node_id} to {new_node_id}")
                                break

                    else:
                        print(f"Pod {pod_id} from {node_id} could not be rescheduled")

                # Clear pods list from the failed node
                node['pods'] = []

    if changed:
        save_nodes_to_file(nodes)
        save_pods(pods)


def update_heartbeat(node_id):
    nodes = load_nodes_from_file()
    if node_id in nodes:
        nodes[node_id]['last_heartbeat'] = datetime.utcnow().isoformat()
        nodes[node_id]['status'] = 'Healthy'
        save_nodes_to_file(nodes)
        return True
    return False

def schedule_pod(pod_id, cpu_request, strategy='first_fit'):
    nodes = load_nodes_from_file()
    pods = load_pods()

    for node_id, node in nodes.items():
        if node['status'] == 'Healthy':
            used_cpu = sum(p['cpu'] for p in node['pods'])
            available_cpu = node['cpu_cores'] - used_cpu

            if available_cpu >= cpu_request:
                # Update node's pod list
                node['pods'].append({'id': pod_id, 'cpu': cpu_request})
                save_nodes_to_file(nodes)

                # Save pod to pods.json
                pods[pod_id] = {
                    'id': pod_id,
                    'cpu': cpu_request,
                    'node_id': node_id,
                    'status': 'Running'
                }
                save_pods(pods)

                return node  # success

    return None  # no fit found

def list_pods():
    return list(load_pods().values())

def delete_pod(pod_id):
    nodes = load_nodes_from_file()
    pods = load_pods()

    if pod_id not in pods:
        return False

    node_id = pods[pod_id]['node_id']

    # Remove pod from the node's pod list
    if node_id in nodes:
        nodes[node_id]['pods'] = [p for p in nodes[node_id]['pods'] if p['id'] != pod_id]
        save_nodes_to_file(nodes)

    # Remove from pods.json
    del pods[pod_id]
    save_pods(pods)

    return True

# Load nodes once on module load
load_nodes_from_file()