## WEEK 1 – API Server & Node Manager

- **Objective:** Implement the base Flask API server and basic node management functionality.
- **Key Features Implemented:**
  - Created the API server using Flask.
  - Developed a Node Manager to handle adding and listing nodes.
- **Commands:**
  - **Start the API server**  
    `python3 api_server/app.py`
  - **Add a node to the cluster**  
    **curl -X POST** [http://localhost:5000/add_node](http://localhost:5000/add_node)
  - **List all registered nodes**  
    **curl -X GET** [http://localhost:5000/list_nodes](http://localhost:5000/list_nodes)

## WEEK 2 – Heartbeat Monitoring & Pod Scheduling

- **Objective:** Implement heartbeat-based node health monitoring and basic pod scheduling.
- **Key Features Implemented:**
  - Created /heartbeat route to receive signals from nodes.
  - Marked nodes as Healthy or Unhealthy based on heartbeat timestamps.
  - Scheduled pods to healthy nodes using a best-fit strategy.
  - Introduced pods.json to persist pod data.
  - Automatically rescheduled pods from unhealthy nodes.

## Week 3 - System Design and Documentation

- **Objective:** Implement a Web Interface where the user can input new pods and new nodes
- **Key Features Implemented:**
  - Listed all the nodes which are created.
  - Made a basic web interface for the user to interact.
  - Handled different edge cases. 