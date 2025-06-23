import streamlit as st
from streamlit_ace import st_ace
from streamlit_agraph import agraph, Node, Edge, Config
import subprocess
import os
import json

st.set_page_config(layout="wide")
st.title("Python Interpreter Playground")

default_code = '''x = 10.5
show(x)

y = yes
show(y)
'''

# Layout: Playground (left) and Output (right)
col1, col2 = st.columns([1, 1])
AST_TYPE_NAMES = {
    0: "Program",
    1: "Block",
    2: "Assign",
    3: "Print",
    4: "Name",
    5: "Int",
    6: "Float",
    7: "Bool",
    8: "None",
    9: "BinaryOp",
    10: "UnaryOp",
    11: "If",
    12: "While",
    # ...add all your types here...
}

with col1:
    st.subheader("Playground")
    code = st_ace(value=default_code, language="python", theme="monokai", height=300)
    run_clicked = st.button("Run code", key="run")
    ast_clicked = st.button("Show AST for code above", key="ast")

code_path = "input.my"
with open(code_path, "w") as f:
    f.write(code)

output = ""
ast_json = None
ast_output = ""

with col2:
    st.subheader("Output")
    if run_clicked:
        result = subprocess.run(
            ["./main", code_path],
            cwd=os.path.abspath("."),
            capture_output=True,
            text=True
        )
        output = result.stdout if result.stdout else result.stderr
        st.code(output)

    if ast_clicked:
        result = subprocess.run(
            ["./main", code_path, "--dump-ast"],
            cwd=os.path.abspath("."),
            capture_output=True,
            text=True
        )
        ast_output = result.stdout if result.stdout else result.stderr
        try:
            ast_json = json.loads(ast_output)
        except Exception:
            ast_json = None
            st.code(ast_output)

# Bottom: AST Tree only (no JSON)
with st.container():
    st.markdown("---")
    st.subheader("AST Tree")
    if ast_clicked and ast_json:
        st.markdown("### AST Tree View")
        def ast_to_graph(node, parent_id=None, nodes=None, edges=None, node_id=[0]):
            if nodes is None: nodes = []
            if edges is None: edges = []
            my_id = str(node_id[0])
            node_type = node.get("type", "unknown")
            type_name = AST_TYPE_NAMES.get(node_type, str(node_type))
            # Compose a label with type and key info
            label = type_name
            # Add more info if available
            for key in ["name", "value", "op"]:
                if key in node:
                    label += f"\n{key}: {node[key]}"
            nodes.append(Node(id=my_id, label=label, size=20))
            if parent_id is not None:
                edges.append(Edge(source=parent_id, target=my_id))
            node_id[0] += 1
            for child in node.get("children", []):
                ast_to_graph(child, my_id, nodes, edges, node_id)
            return nodes, edges
        nodes, edges = ast_to_graph(ast_json)
        config = Config(
            width=1200,
            height=600,
            directed=True,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=True,
            hierarchical=True,
            hierarchical_sort_method='directed',
            hierarchical_direction='UD'  # 'UD' means Up to Down (vertical)
        )
        agraph(nodes=nodes, edges=edges, config=config)



def ast_to_graph(node, parent_id=None, nodes=None, edges=None, node_id=[0]):
    if nodes is None: nodes = []
    if edges is None: edges = []
    my_id = str(node_id[0])
    node_type = node.get("type", "unknown")
    type_name = AST_TYPE_NAMES.get(node_type, str(node_type))
    label = type_name
    for key in ["name", "value", "op"]:
        if key in node:
            label += f"\n{key}: {node[key]}"
    nodes.append(Node(id=my_id, label=label, size=20))
    if parent_id is not None:
        edges.append(Edge(source=parent_id, target=my_id))
    node_id[0] += 1
    for child in node.get("children", []):
        ast_to_graph(child, my_id, nodes, edges, node_id)
    return nodes, edges