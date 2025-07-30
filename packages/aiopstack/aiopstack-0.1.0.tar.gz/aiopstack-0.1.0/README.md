# AIOpStack

[![Python ≥3.8](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![LangChain v0.3.25](https://img.shields.io/badge/LangChain-0.3.25-blue.svg)](https://pypi.org/project/langchain/)
[![LangGraph v0.4.8](https://img.shields.io/badge/LangGraph-0.4.8-orange.svg)](https://pypi.org/project/langgraph/)
[![LangChain MCP Adapters v0.1.7](https://img.shields.io/badge/LangChain--MCP--Adapters-0.1.7-purple.svg)](https://pypi.org/project/langchain-mcp-adapters/)

---

AIOpStack is a collection of AI Operational Agents built with Langchain/LangGraph and Streamlit‑based GUI for operational interaction and visualization.

🌐 [English](README.md) | [简体中文](README.zh.md)

### 🎯 Motivation

1. **Fast‑boot** – DevOps and sysadmins often test multiple MCPs for automation, but setup can be time‑consuming. AIOpStack drastically reduces study and setup time.  
2. **Lightweight** – IDEs like Cursor and VSCode with Cline are powerful but resource‑heavy. AIOpStack stays minimal and nimble.  
3. **Local Deployments** – Deploy locally to access private environments.  
4. **Free & Open** – Fully open‑source, no vendor lock‑in or licensing fees.

### 🚀 Features

- **OpenAI‑compatible LLM API integration** – Connect to any OpenAI‑compatible LLM endpoint.  
- **MCP integration** – Seamless bridge between LLMs and popular MCP tools (e.g., Kubernetes, Ansible).  
- **Human‑in‑the‑loop feedback** – Pause for confirmation or iterative refinement at key steps.  
- **Pure Python & GUI‑free** – Fully Python‑powered: no frontend skills required for reuse or extension.

### 📖 Quick Start

#### Requirements

- Python 3.8+  
- OpenAI‑compatible LLM API URL & Key

#### Installation

```bash
pip install aiopstack
```

#### Usage Examples
```bash
# QuickStart, the project will be listening at 0.0.0.0:8051
aiops
```

## 🤝 Contributing

We welcome contributions! If you have suggestions or feature requests, feel free to open an issue or submit a pull request.

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/ohtaman/streamlit-desktop-app.git
```

2. Install dependencies:

```bash
cd src/aiopstack
pip install -r requirements.txt
```

3. Run Streamlit
```bash
streamlit run app.py
```


