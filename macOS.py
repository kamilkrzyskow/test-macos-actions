import os
from ctypes.macholib import dyld
from itertools import chain

library_names = ("cairo-2", "cairo", "libcairo-2")
filenames = ("libcairo.so.2", "libcairo.2.dylib", "libcairo-2.dll")
found_path = ""
names = []

for name in library_names:
    names += [
        'lib%s.dylib' % name,
        '%s.dylib' % name,
        '%s.framework/%s' % (name, name)
    ]

for name in names:
    for path in dyld.dyld_image_suffix_search(
        chain(
            dyld.dyld_override_search(name),
            dyld.dyld_executable_path_search(name),
            dyld.dyld_default_search(name)
        )
    ):
        print(path)
        if os.path.isfile(path):
            found_path = path
            break
        try:
            if dyld._dyld_shared_cache_contains_path(path):
                found_path = path
                break
        except NotImplementedError:
            pass
    if found_path:
        filenames = (found_path, ) + filenames
        break
else:
    found_path = "not found"

print(f"The path is {found_path}")
print("List of files that FFI will try to load:")
for filename in filenames:
    print("-", filename)
