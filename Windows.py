import os

library_names = ("cairo-2.dll", "cairo.dll", "libcairo-2.dll")
filenames = ("libcairo.so.2", "libcairo.2.dylib", "libcairo-2.dll")
found_path = ""

for name in library_names:
    for path in os.environ['PATH'].split(os.pathsep):
        resolved_path = os.path.join(path, name)
        print(resolved_path)
        if os.path.exists(resolved_path):
            filenames = (resolved_path, ) + filenames
            found_path = resolved_path
            break
    if found_path:
        break
else:
    found_path = "not found"

print(f"The path is {found_path}")
print("List of files that FFI will try to load:")
for filename in filenames:
    print("-", filename)
