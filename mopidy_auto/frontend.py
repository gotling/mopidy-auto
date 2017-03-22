import pykka

from mopidy import core


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.core = core

    # Your frontend implementation