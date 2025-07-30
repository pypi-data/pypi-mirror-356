import importlib
import sys

root_pkg = __name__.split("._vendor", 1)[0]
vendored_name = f"{root_pkg}._vendor.paapi5_python_sdk"

pkg = importlib.import_module(vendored_name)

sys.modules.setdefault("paapi5_python_sdk", pkg)