import inspect
import os
import shutil
import subprocess
from ctypes import util

print(f"\n---Running {os.path.basename(__file__)}---\n")


class Meta(type):
    def __getattribute__(self, attr):
        att = super().__getattribute__(attr)
        print("Meta__getattribute__:", att)
        return att


class CustomPopen(subprocess.Popen, metaclass=Meta):

    def __init__(self, *args, **kwargs):
        print(f"Subprocess command:\n  {' '.join(args[0])}")
        super().__init__(*args, **kwargs)

    def communicate(self, *args, **kwargs):
        out, _ = super().communicate(*args, **kwargs)
        out = out.rstrip()
        print("Subprocess output:")
        if out:
            print(f"  {os.fsdecode(out)}")
        else:
            print(f"  Output is empty")
        return out, _

    def __class_getitem__(cls, item):
        item = super().__class_getitem__(item)
        print("__class_getitem__:", item)
        return item

    def __getattr__(self, item):
        att = super().__getattr__(item)
        print("__getattr__:", att)
        return att

    def __get_attribute__(self, name_):
        att = super().__getattribute__(name_)
        print("__getattribute__:", att)
        if name_ == "stdout":
            print("Subprocess output:")
            for line_ in att:
                print(os.fsdecode(line_))
        return att


subprocess.Popen = CustomPopen

print("ctypes.util script with the find_library:")
print(inspect.getsourcefile(util.find_library), end="\n\n")

print("find_library function:")
func_lines = list(map(str.rstrip, inspect.getsourcelines(util.find_library)[0]))
indent = len(func_lines[0]) - len(func_lines[0].lstrip())
for line in func_lines:
    print(line.replace(" " * indent, "", 1))

library_names = ("cairo-2", "cairo", "libcairo-2")
filenames = ("libcairo.so.2", "libcairo.2.dylib", "libcairo-2.dll")
c_compiler = shutil.which("gcc") or shutil.which("cc")
ld_env = os.environ.get("LD_LIBRARY_PATH")
first_found = ""

print("\nLD_LIBRARY_PATH =", ld_env, end="\n\n")

for name in library_names:
    if hasattr(util, "_findSoname_ldconfig"):
        result = util._findSoname_ldconfig(name)
        print(f"_findSoname_ldconfig({name}) ->", result)
        if result:
            print(f"Found {result}")
            if not first_found:
                first_found = result
        print("---")
    if c_compiler and hasattr(util, "_findLib_gcc"):
        result = util._findLib_gcc(name)
        print(f"_findLib_gcc({name}) ->", result)
        if result and hasattr(util, "_get_soname"):
            result = util._get_soname(result)
        if result:
            print(f"Found {result}")
            if not first_found:
                first_found = result
        print("---")
    if hasattr(util, "_findLib_ld"):
        result = util._findLib_ld(name)
        print(f"_findLib_ld({name}) ->", result)
        if result and hasattr(util, "_get_soname"):
            result = util._get_soname(result)
        if result:
            print(f"Found {result}")
            if not first_found:
                first_found = result
        print("---")
    if hasattr(util, "_findLib_crle"):
        result = util._findLib_crle(name, False)
        print(f"_findLib_crle({name}) ->", result)
        if result and hasattr(util, "_get_soname"):
            result = util._get_soname(result)
        if result:
            print(f"Found {result}")
            if not first_found:
                first_found = result
        print("---")

if first_found:
    filenames = (first_found,) + filenames

print(f"The path is {first_found or 'not found'}")
print("List of files that FFI will try to load:")
for filename in filenames:
    print("-", filename)
