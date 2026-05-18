from ._interface import Listener
from ._protected_change import ProtectedChangeListener


class ChangeListener(ProtectedChangeListener, Listener):
    pass
