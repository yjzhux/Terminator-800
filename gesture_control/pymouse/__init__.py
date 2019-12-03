'''Work for mac and unix'''

import sys

elif sys.platform == 'darwin':
    from mac import PyMouse, PyMouseEvent
else:
    from unix import PyMouse, PyMouseEvent

