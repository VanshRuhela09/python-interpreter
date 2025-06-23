import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os

st.set_page_config(layout="wide")
st.title("Python Interpreter Playground")

default_code = '''x = 10.5
show(x)

y = yes
show(y)
'''

# Code editor
code = st_ace(value=default_code, language="python", theme="monokai", height=300)

# Run button
if st.button("Run code above"):
    # Save code to a temp file
    code_path = "input.my"
    with open(code_path, "w") as f:
        f.write(code)
    # Run the interpreter
    result = subprocess.run(
        ["./main", code_path],
        cwd=os.path.abspath("."),
        capture_output=True,
        text=True
    )
    output = result.stdout if result.stdout else result.stderr
    st.markdown("### Output")
    st.code(output)