import logging

logger = logging.getLogger(__name__)

logger.debug("Get templates")

header_info = """# Produced by pyarchetype template
# pip install pyarchetype
# git clone https://github.com/redcorjo/pyarchetype.git"""

templates_files = [
    {
        "path": ".vscode/tasks.json",
        "content": """
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "compile_and_upload",
            "type": "shell",
            "command": "${workspaceFolder}/scripts/compile_and_upload.sh"
        },
        {
            "label": "compile_only",
            "type": "shell",
            "command": "${workspaceFolder}/scripts/compile_only.sh"
        },
        {
            "label": "upload_pypi",
            "type": "shell",
            "command": "${workspaceFolder}/scripts/upload_pypi.sh"
        },
        {
            "label": "echo",
            "type": "shell",
            "command": "echo Hello"
        }
    ]
}
"""
    },
    {
        "path": ".vscode/launch.json",
        "content": """
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: {{app}} main File",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/{{ app }}/{{ app }}.py",
            "args": [],
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
""",
    },
    {
        "path": ".gitignore",
        "content": """
{{ header_info }}
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
src/{{ app }}.egg-info
.pypirc
 """,
    },
    {
        "path": "pyproject.toml",
        "content": """
{{ header_info }}
[project]
name = "{{ app }}"
version = "{{initial_version}}"
description = "Your dummy {{ app }}"
authors = [
  { name="{{ name }}", email="{{ email }}" },
]
readme = "README.md"
requires-python = ">={{python_version}}"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/user/{{app}}"
"Bug Tracker" = "https://github.com/user/{{app}}/issues"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.scripts]
pyarchetype = "{{ app }}.{{ app }}:main"
""",
    },
    {
        "path": "LICENSE",
        "content": """
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    },
    {
        "path": "README.md",
        "content": """
# {{app}}

## Description 

Your dummy {{ app }}

## Author

Name: {{ name }} 
Email: {{ email }}


Version: {{initial_version}}
""",
    },
    {"path": "requests.txt", "content": ""},
    {
        "path": "scripts/compile_and_upload.sh",
        "content": """
#!/bin/bash
{{ header_info }}

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python{{python_version}}
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo "Cleanup old dist files"
test -e ${BASE_DIR}/dist/*.whl && rm ${BASE_DIR}/dist/* 

if ! test -e ${BASE_DIR}/.venv/bin/activate
then
    echo "Creating default virtual environment"
    ${PYTHON} -m venv .venv
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
    python -m pip install --upgrade pip build twine
else
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
fi

echo "Build"
python -m build

echo "Upload to pypi"
if test -e ${TWINE_CONFIG}
then
    chmod 600 ${TWINE_CONFIG}
    twine upload dist/${PACKAGE}* --config-file ${TWINE_CONFIG} 
else
    twine upload dist/*
fi

python -m pip install --upgrade dist/${PACKAGE}*whl

#{{ app }} -h

exit
""",
    },
    {
        "path": "scripts/compile_only.sh",
        "content": """
#!/bin/bash
{{ header_info }}

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python{{python_version}}
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo "Cleanup old dist files"
test -e ${BASE_DIR}/dist/*.whl && rm ${BASE_DIR}/dist/* 

if ! test -e ${BASE_DIR}/.venv/bin/activate
then
    echo "Creating default virtual environment"
    ${PYTHON} -m venv .venv
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
    python -m pip install --upgrade pip build twine
else
    echo "Enable virtual environment"
    source ${BASE_DIR}/.venv/bin/activate
fi

echo "Build"
python -m build

python -m pip install --upgrade dist/${PACKAGE}*whl

#{{app}} -h

exit
""",
    },
    {
        "path": "scripts/upload_pypi.sh",
        "content": """
#!/bin/bash
{{ header_info }}

BASE_DIR=$(dirname $0)/..
TWINE_CONFIG=$(dirname $0)/../.pypirc
PYTHON=python{{ python_version }}
PACKAGE=pyarchetype

cd ${BASE_DIR}

echo "Upload to pypi"
if test -e ${TWINE_CONFIG}
then
    chmod 600 ${TWINE_CONFIG}
    twine upload dist/${PACKAGE}* --config-file ${TWINE_CONFIG} 
else
    twine upload dist/*
fi

python -m pip install --upgrade dist/${PACKAGE}*whl

#{{ app }} -h

exit
""",
    },
    {"path": "tmp"},
    {"path": "scripts"},
    {"path": "tests"},
]
