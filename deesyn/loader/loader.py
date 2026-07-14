from __future__ import annotations

import os.path
import importlib.util
from discord.ext import commands


class Loader:
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

        self.modules = []
        # path
        self.root_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),'..','..'
            )
        )

    def get_modules_class(self):

        self.modules.clear()

        modules_dir = os.path.join(self.root_dir,'modules')
        for module in os.scandir(modules_dir):

            if not module.is_dir():
                continue
            module_dir = module.path
            entry_point = os.path.join(module_dir, "entry_point.py")
            spec = importlib.util.spec_from_file_location(module.name, entry_point)

            if spec is None or spec.loader is None:
                continue

            py_module = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(py_module)
            except Exception as e:
                print(f"Failed to import {module.name}: {e}")
                continue

            if hasattr(py_module, "CONFIG"):
                _class_name = getattr(py_module, "CONFIG").get("main_class", None)
                if _class_name:
                    _class = getattr(py_module, _class_name)
                    self.modules.append(_class)

                    continue
            default_class = py_module.__name__.capitalize()

            if not hasattr(py_module, default_class):
                print(f"Module: {py_module} Load Failed, Class not found")
                continue
            _class = getattr(py_module, default_class)
            self.modules.append(_class)

    async def import_modules(self):
        for module in self.modules:
            try:
                await self.bot.add_cog(module(self.bot))
            except Exception as e:
                print(e)
                print(f"Failed to load module: {module}")
            else:
                print(f"Loaded module: {module}")

    async def start_loader(self,sync=False):
        print("start loader")
        self.get_modules_class()
        print(
            f"{len(self.modules)} "
            f"{'modules' if len(self.modules) != 1 else 'module'}"
        )
        await self.import_modules()
        total_cog = None
        if sync:
            print("Start sync")
            total_cog = await self.bot.tree.sync()
            print("Sync completed")
        print("Load completed")
        return total_cog
