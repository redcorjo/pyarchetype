import logging

logger = logging.getLogger(__name__)

logger.debug("Get templates")

templates_files = [
    {
        "path": ".gitignore",
        "content": """
# Editors
.vscode/
.idea/

# Vagrant
.vagrant/

# Mac/OSX
.DS_Store

# Windows
Thumbs.db

dist
tmp
.vscode
.venv
*.pyc
src/pyarchetype.egg-info
.pypirc
 """,
    },
    {"path": "pyproject.toml", "content": ""},
    {"path": "LICENSE", "content": ""},
    {"path": "README.md", "content": ""},
    {"path": "requests.txt", "content": ""},
    {"path": "tmp"},
    {"path": "scripts"},
    {"path": "tests"},
]
