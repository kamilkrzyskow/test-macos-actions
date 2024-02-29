import inspect
from ctypes.util import find_library

print("find_library script:")
print(inspect.getsourcefile(find_library))
print("\nfind_library function:")
print(inspect.getsource(find_library))
