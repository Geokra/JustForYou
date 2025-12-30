import importlib.util
import inspect
import os
import pathlib
import sys

from module.module import Module

class ModuleManager:

    def __init__(self):
        self.modules = dict()
        self.directory = None
        self.module_extension = self.determine_module_extension()

    def set_directory(self, directory: pathlib.Path):
        self.directory = directory
        if not directory.exists():
            directory.mkdir()

    def load(self):
        for file in self.directory.glob(f"*.{self.module_extension}"):
            module_name = self.normalize_module_name(file)
            module = self.load_module(module_name, file)
            instance = self.create_module_instance(module)
            self.modules[module_name] = instance

    def enable(self):
        for module in self.modules.values():
            module.on_enable()

    def disable(self):
        for module in self.modules.values():
            module.on_disable()

    def normalize_module_name(self, file: pathlib.Path):
        module_name = file.name
        if ".cpython" in file.name:
            module_name = file.name.split(".cpython")[0]
        return module_name

    def load_module(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def create_module_instance(self, module):
        for key, member, in inspect.getmembers(module, inspect.isclass):
            if issubclass(member, Module) and member is not Module:
                return member()
        print(f"No Module subclass found in {module}")
        return None

    @staticmethod
    def determine_module_extension():
        if os.name == "posix":
            return "so"
        if os.name == "nt":
            return "pyd"
        return None

