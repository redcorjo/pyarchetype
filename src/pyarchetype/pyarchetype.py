import argparse
import os
import logging
import sys
import venv
from jinja2 import Template
import importlib_metadata
try:
    from templates.templates import templates_files
except:
    from pyarchetype.templates.templates import templates_files
#import templates.templates as template_files

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


__version__ = importlib_metadata.version("pyarchetype")


class PyArchetype:

    templates = templates_files

    def __init__(self):
        self.__settings = self.get_flags()
        path = self.__settings.path
        logger.debug(f"Create structure at path {path}")
        self.create_Structure(path)

    def get_flags(self):
        parser = argparse.ArgumentParser(
            prog="pyarchetype",
            description=f"Tool to create the skeleton of a python project. Version {__version__}",
        )
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + __version__
        )
        parser.add_argument(
            "--path", type=str, help="basedir. Default current dir", required=False, default=os.getcwd()
        )
        parser.add_argument(
            "--module",
            type=str,
            help="Module name . Default value is app",
            required=False,
            default="app",
        )
        parser.add_argument(
            "--force_overwrite",
            help="Force overwrite. Default value is false",
            required=False,
            action="store_true",
        )
        parser.add_argument(
            "--create_venv",
            help="Create project virtualenv. Default value is false",
            required=False,
            action="store_true",
        )
        try:
            settings = parser.parse_args()
        except Exception as e:
            #parser.print_help()
            sys.exit(1)
        logger.info(settings)
        return settings

    def create_Structure(self, path):
        logger.debug(f"Creating skeleton at path {path}")
        if not os.path.exists(path):
            logger.info(f"Creating basedir {path}")
            os.makedirs(path)
        else:
            logger.info(f"basedir {path} already exists")
        if self.__settings.create_venv == True:
            self.create_Virtual_Env(path)
        self.create_Main_Skeleton(path, force_overwrite=self.__settings.force_overwrite)
        self.create_Src_App(path)
        return True

    def create_Virtual_Env(self, path):
        my_venv = os.path.join(path, ".venv")
        if not os.path.exists(my_venv) or self.__settings.force_overwrite == True:
            logger.debug("Creating virtual env")
            venv.create(my_venv, with_pip=True)

        return True

    def create_Src_App(self, path):
        basedir = os.path.join(path, "src", self.__settings.module)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filename = os.path.join(basedir, self.__settings.module + ".py")
        data = """
import logging, os

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

def main():
    logger.debug("Main")
    
if __name__ == "__main__":
    main()

        """
        self.__create_file(
            filename, data, force_overwrite=self.__settings.force_overwrite
        )
        filename = os.path.join(basedir, "__init__.py")
        data = """
        """
        self.__create_file(
            filename, data, force_overwrite=self.__settings.force_overwrite
        )
        return True

    def create_Main_Skeleton(self, path, force_overwrite=False):
        for item in self.templates:
            filename = os.path.join(path, item["path"])
            if "content" in item:
                template = item["content"]
                jinja_template = Template(template)
                content = jinja_template.render(app="app", email="user@email.com", name="User")
                self.__create_file(filename, content, force_overwrite=force_overwrite)
            else:
                if not os.path.exists(filename):
                    logger.info(f"Creating folder {filename}")
                    os.makedirs(filename)
        return True

    def __create_file(self, filename, data, force_overwrite=False):
        if force_overwrite == True or not os.path.exists(filename):
            with open(filename, "w") as output:
                logger.info(f"Updating file {filename}")
                output.write(data)


def main():
    logger.debug(f"PyArchetype. Version {__version__}")
    pyarchetype = PyArchetype()
    logger.debug("Done")


if __name__ == "__main__":
    main()
