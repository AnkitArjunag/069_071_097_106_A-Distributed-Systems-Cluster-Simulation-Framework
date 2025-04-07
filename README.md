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
