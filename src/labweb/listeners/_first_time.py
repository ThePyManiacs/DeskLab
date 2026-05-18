from ._interface import Listener
from ._protected_first_time import ProtectedFirstTimeListener


class FirstTimeListener(ProtectedFirstTimeListener, Listener):
    pass
