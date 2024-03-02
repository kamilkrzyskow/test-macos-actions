import inspect
import os
import re
import subprocess
from ctypes.util import (
    _findLib_gcc,
    _findLib_ld,
    _findSoname_ldconfig,
    _get_soname,
    _is_elf,
)

library_names = ("cairo-2", "cairo", "libcairo-2")
filenames = ("libcairo.so.2", "libcairo.2.dylib", "libcairo-2.dll")
found_path = ""

print(inspect.getsource(_findLib_gcc))
print("---")
print(inspect.getsource(_findLib_ld))
print("---")
print(inspect.getsource(_findSoname_ldconfig))
print("---")

libpath = os.environ.get('LD_LIBRARY_PATH')
print("LD_LIBRARY_PATH =", libpath)

for name in library_names:
    expr = r'[^\(\)\s]*lib%s\.[^\(\)\s]*' % re.escape(name)
    command = ['ld', '-t']
    if libpath:
        for d in libpath.split(':'):
            command.extend(['-L', d])
    command.extend(['-o', os.devnull, '-l%s' % name])
    print("Running", " ".join(command))
    try:
        out, _ = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ).communicate()
        result = re.findall(expr, os.fsdecode(out))
        print("  Result", "\n".join(result) or "is empty")
        if not result:
            continue
        for path in result:
            if not _is_elf(path):
                continue
            path = os.fsdecode(path)
            found_path = _get_soname(path)
            filenames = (found_path, ) + filenames
            break
    except Exception as err:
        print("  Error during ld command:", err)
    if found_path:
        break
else:
    found_path = "not found"

print(f"The path is {found_path}")
print("List of files that FFI will try to load:")
for filename in filenames:
    print("-", filename)
