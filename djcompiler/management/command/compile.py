from configparser import ConfigParser
from djcompiler.management.command import BaseCommand
from djcompiler.management.command import buildfile
from djcompiler.compiler.djcompiler import DjangoCompiler
import sys


class CompileProject(BaseCommand):
    config: dict = {}
    description: str = "\n\tThis command compile the django project \n\tNOTE: Run it in project working directory."

    def intial_configs(self):
        try:
            parser = ConfigParser(
                interpolation=None, delimiters=("=",), comment_prefixes=("#",), strict=False
            )
            parser.optionxform = str
            with open(".djcompiler", "r", encoding="utf-8") as f:
                parser.read_string("[djcompiler]\n" + f.read())
            list_options = {"ignored_dirs", "ignored_files", "other_dirs_needed", "other_files_needed"}
            self.config = {
                key: value.split() if key in list_options else value
                for key, value in parser.items("djcompiler")
            }
        except FileNotFoundError as e:
            print("The config file couldn't be found type 1 to create it or 0 to finish")
            try:
                build_file = input(">>> ")
            except EOFError:
                build_file = 0
            if build_file == "1":
                config_file = buildfile.BuildFile()
                config_file.execute()
                self.intial_configs()
                print("ReInitial the configs again")
            if build_file == "0":
                exit()

    def execute(self):
        self.intial_configs()
        build_dir_check = self.config.get("build_directory", False)
        build_dir = build_dir_check if build_dir_check else "build"
        sys.argv = ['setup.py', 'build_ext', '--build-lib', f"{build_dir}"]
        compiler = DjangoCompiler(**self.config)
        compiler.compile_project()






