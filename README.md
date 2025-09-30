# Clone the repository

git clone `<your-repository-url>`
cd `<project-directory>`

# Create virtual environment

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies

pip install -r requirements.txt

### Start Development Server

```bash
streamlit run main.py
```

### Start MCP Server

mcp dev mcp_server.py

(Need to install node+uv)
