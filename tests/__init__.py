from sys import version_info

if version_info[0] >= 3:
    from .basic_3 import *
else:
    from .basic_2 import *