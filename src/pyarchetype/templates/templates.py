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
    {"path": "pyproject.toml", "content": """
[project]
name = "{{ app }}"
version = "0.0.1"
description = "Your dummy {{ app }}"
authors = [
  { name="{{ name }}", email="{{ email }}" },
]
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/user/app"
"Bug Tracker" = "https://github.com/user/app/issues"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.scripts]
pyarchetype = "{{ app }}.{{ app }}:main"
"""},
    {"path": "LICENSE", "content": ""},
    {"path": "README.md", "content": ""},
    {"path": "requests.txt", "content": ""},
    {"path": "tmp"},
    {"path": "scripts"},
    {"path": "tests"},
]
