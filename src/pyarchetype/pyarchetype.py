import argparse
import os
import logging
import sys
import venv
from jinja2 import Template
import importlib_metadata
try:
    from templates.templates import templates_files, header_info
except:
    from pyarchetype.templates.templates import templates_files
#import templates.templates as template_files

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


try:
    __version__ = importlib_metadata.version("pyarchetype")
except:
    __version__ = "x.y.z"


class PyArchetype:

    templates = templates_files

    def __init__(self):
        self.__settings = self.get_flags()
        if self.__settings.wizard == True:
            self.wizard_task()
        if self.__settings.create == True:
            logger.debug(f"Create structure at path {self.__settings.path}")
            self.create_structure(self.__settings.path)

    def wizard_task(self):
        logger.info("Winzard ....")
        settings = vars(self.__settings)
        for key, value in settings.items():
            if key != "wizard":
                new_value = str ( input(f"value for {key}. Default value is {value}:  ") or value )
                if isinstance(value, bool):
                    if new_value in ("True", "true", "TRUE", 1):
                        new_value = True
                    else:
                        new_value = False
                # else:
                #     new_value = str ( input(f"value for {key}. Default value is {value}:  ") or value )
                settings[key] = new_value
                logger.info("item")

    def get_flags(self):
        parser = argparse.ArgumentParser(
            prog="pyarchetype",
            description=f"Tool to create the skeleton of a python project. Version {__version__}",
        )
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + __version__
        )
        parser.add_argument(
            "--create",
            help="Create skeleton structure of your python project",
            required=False,
            action="store_true",
        )
        parser.add_argument(
            "--wizard",
            help="Define all parameters in wizard mode",
            required=False,
            action="store_true",
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
            "--name",
            type=str,
            help="Owner. Default value is user",
            required=False,
            default="user",
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Email address. Default value is user@email.com",
            required=False,
            default="user@email.com",
        )
        parser.add_argument(
            "--initial_version",
            type=str,
            help="Initial Version. Default value is 0.0.1",
            required=False,
            default="0.0.1",
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
        if settings.create == False:
            parser.print_help()
        else:
            all_flags = vars(settings)
            logger.info(f"all_flags={all_flags}")
        return settings

    def create_structure(self, path):
        logger.debug(f"Creating skeleton at path {path}")
        if not os.path.exists(path):
            logger.info(f"Creating basedir {path}")
            os.makedirs(path)
        else:
            logger.info(f"basedir {path} already exists")
        if self.__settings.create_venv == True:
            self.create_virtual_env(path)
        self.create_main_skeleton(path, force_overwrite=self.__settings.force_overwrite)
        self.create_src_app(path)
        self.create_test_app(path)
        return True

    def create_virtual_env(self, path):
        my_venv = os.path.join(path, ".venv")
        if not os.path.exists(my_venv) or self.__settings.force_overwrite == True:
            logger.debug("Creating virtual env")
            venv.create(my_venv, with_pip=True)

        return True

    def create_src_app(self, path):
        basedir = os.path.join(path, "src", self.__settings.module)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filename = os.path.join(basedir, self.__settings.module + ".py")
        data = f"""{header_info}
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

    def create_test_app(self, path):
        basedir = os.path.join(path, "tests", self.__settings.module)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filename = os.path.join(basedir, "test_" + self.__settings.module + ".py")
        data = f"""# Test scripts
{header_info}
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
        return True

    def create_main_skeleton(self, path, force_overwrite=False):
        for item in self.templates:
            filename = os.path.join(path, item["path"])
            if "content" in item:
                template = item["content"]
                jinja_template = Template(template)
                template_variables={
                    "app": self.__settings.module,
                    "initial_version": self.__settings.initial_version,
                    "email": self.__settings.email,
                    "name": self.__settings.name,
                    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
                    "header_info": header_info
                }
                content = jinja_template.render(**template_variables)
                self.__create_file(filename, content, force_overwrite=force_overwrite)
            else:
                if not os.path.exists(filename):
                    logger.info(f"Creating folder {filename}")
                    os.makedirs(filename)
        return True

    def __create_file(self, filename, data, force_overwrite=False):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
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
