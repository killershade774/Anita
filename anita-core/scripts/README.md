# 🧰 Anita Bootstrap Installer

Welcome to Anita’s modular bootstrap script! This installer helps contributors and users selectively install only the subsystems they need. Perfect for keeping things lightweight, versioned, and flexible.

## 🚀 Purpose
Anita is built with modularity in mind. Instead of installing **all** dependencies up front, this script lets you choose which components to install—ideal for development, testing, or customizing your build.

## 📂 Structure
The installer reads from multiple `requirements-*.txt` files that map to Anita's core subsystems:

- `requirements-core.txt`: Core architecture and system-level utilities
- `requirements-nlp.txt`: Natural language processing modules
- `requirements-gui.txt`: Graphical interface libraries
- `requirements-reasoning.txt`: Reasoning models and logic engines
- `requirements-extras.txt`: Optional tools, visualizers, etc.

Feel free to customize or add new subsystems as Anita grows.

## 🧪 Usage

Run the script from the project root:

```bash
python scripts/bootstrap.py