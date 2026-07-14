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
        modules_dir = os.path.join(self.root_dir,'modules')
        modules = os.listdir(modules_dir)
        for module in modules:
            class_name = module
            module_dir = os.path.join(modules_dir,module)
            entry_point = os.path.join(module_dir, "entry_point.py")
            spec = importlib.util.spec_from_file_location(class_name, entry_point)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "CONFIG"):
                _class_name = getattr(module, "CONFIG").get("main_class", None)
                if _class_name:
                    _class = getattr(module, _class_name)
                    self.modules.append(_class)

                    continue
            if not hasattr(module, str(class_name).capitalize()):
                print(f"Module: {module} Load Failed, Class not found")
                continue
            _class = getattr(module, str(class_name).capitalize())
            self.modules.append(_class)

    async def import_modules(self):
        for module in self.modules:
            try:
                await self.bot.add_cog(module(self.bot))
            except Exception as e:
                print(e)
                print(f"Failed to load module: {module}")
                continue
            finally:
                print(f"Loaded module: {module}")

    async def start_loader(self,sync=False):
        print("start loader")
        print(f"{len(self.modules)} {"modules" if len(self.modules) > 1 else "module"}")
        self.get_modules_class()
        await self.import_modules()
        total_cog = None
        if sync:
            print("Start sync")
            total_cog = await self.bot.tree.sync()
            print("Sync completed")
        print("Load completed")
        return total_cog