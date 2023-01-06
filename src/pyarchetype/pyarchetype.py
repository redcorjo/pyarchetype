
import argparse
import os
import logging
import sys

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

VERSION = "0.0.3"

class PyArchetype():
    
    templates = [
        {"path": ".gitignore", "content": """
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
         """},
        {"path": "pyproject.toml", "content": ""},
        {"path": "LICENSE", "content": ""},
        {"path": "README.md", "content": ""},
        {"path": "requests.txt", "content": ""},
        {"path": "tmp"},
        {"path": "scripts"},
        {"path": "tests"}
    ]
    
    def __init__(self):
        self.__settings = self.get_flags()
        path = self.__settings.path
        logger.debug(f"Create structure at path {path}")
        self.create_Structure(path)
        
    def get_flags(self):
        parser = argparse.ArgumentParser(prog="pyarchetype", description="Tool to create the skeleton of a python project")
        parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
        parser.add_argument("--path", type=str, help="basedir", required=False, default=os.getcwd())
        parser.add_argument("--module", type=str, help="Module name . Default value is app", required=False, default="app")
        parser.add_argument("--force_overwrite", help="Force overwrite. Default value is false", required=False, action='store_true')
        try:
            settings = parser.parse_args()
        except:
            parser.print_help()
            sys.exit(1)
        logger.debug(settings)
        return settings
    
    def create_Structure(self, path):
        logger.debug(f"Creating skeleton at path {path}")
        if not os.path.exists(path):
            logger.info(f"Creating basedir {path}")
            os.makedirs(path)
        else:
            logger.info(f"basedir {path} already exists")
        self.create_Main_Skeleton(path, force_overwrite=self.__settings.force_overwrite)
        self.create_Src_App(path)
        return True
    
    def create_Src_App(self, path):
        basedir = os.path.join(path, "src", self.__settings.module)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filename = os.path.join(basedir,  self.__settings.module + ".py")
        data="""
        """
        self.__create_file(filename, data, force_overwrite=self.__settings.force_overwrite)
        filename = os.path.join(basedir, "__init__.py")
        data="""
        """
        self.__create_file(filename, data, force_overwrite=self.__settings.force_overwrite)
        return True
    
    def create_Main_Skeleton(self, path, force_overwrite=False):
        for item in self.templates:
            filename = os.path.join(path, item["path"])
            if "content" in item:
                content = item["content"]
                self.__create_file(filename, content, force_overwrite=force_overwrite)
            else:
                if not os.path.exists(filename):
                    logger.info(f"Creating folder {filename}")
                    os.makedirs(filename)
        return True
            
    def __create_file(self, filename, data, force_overwrite=False):
        if force_overwrite == True or not os.path.exists(filename):
            with open(filename, 'w') as output:
                logger.info(f"Updating file {filename}")
                output.write(data)
def main():
    logger.debug("PyArchetype")
    pyarchetype = PyArchetype()
    logger.debug("Done")   

if __name__ == "__main__":
    main()