import importlib.util
import json
import os
import pathlib
import sys
import zipimport

class ModuleManager:

    def __init__(self, debug: bool = False):
        self.modules = dict()
        self.directory = None
        self.module_extension = "module"
        self.debug: bool = debug

    def set_directory(self, directory: pathlib.Path):
        self.directory = directory
        if not directory.exists():
            directory.mkdir()

    def load(self):
        if self.debug:
            for dir in self.directory.iterdir():
                module_name, class_name, file = self._load_module_entry_from_file(dir.joinpath("module.json"))
                file = dir.joinpath(file)
                self._load_module(module_name, class_name, file)
            return
        for file in self.directory.glob(f"*.{self.module_extension}"):
            importer = zipimport.zipimporter(str(file))
            sys.path.insert(0, str(file))
            raw_data = importer.get_data(f"{file}/module.json")
            module_name, class_name, entry_file = self._load_module_entry_from_bytes(raw_data)
            self._load_module(module_name, class_name, f"{file}/{entry_file}", importer)


    def _load_module_entry_from_file(self, path: pathlib.Path):
        with open(path) as file:
            data = json.load(file)
        name = data['name']
        class_name = data['class']
        file = data['file']
        return name, class_name, file

    def _load_module_entry_from_bytes(self, raw_data: bytes):
        data = json.loads(raw_data.decode())
        name = data['name']
        class_name = data['class']
        file = data['file']
        return name, class_name, file

    def _load_module(self, module_name, class_name, file, importer=None):
        if importer:
            module = self.load_module_from_zip(importer, module_name, file)
        else:
            module = self.load_module(module_name, file)
        instance = self.create_module_instance(module, class_name)
        self.modules[module_name] = instance

    def enable(self):
        for module in self.modules.values():
            module.on_enable()

    def disable(self):
        for module in self.modules.values():
            module.on_disable()


    def load_module(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def load_module_from_zip(self, importer, module_name, file_path):
        spec = importlib.util.spec_from_loader(module_name, importer, origin=file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def create_module_instance(self, module, class_name: str):
        clazz = getattr(module, class_name)
        if clazz is not None:
            return clazz()
        print(f"No Module class found in {module}")
        return None
