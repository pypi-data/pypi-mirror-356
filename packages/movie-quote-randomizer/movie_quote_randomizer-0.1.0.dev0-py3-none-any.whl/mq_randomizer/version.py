from . import __summary__, __title__, __version__


class MQRAbout:

    def __init__(self):
        self.version = __version__
        self.title = __title__
        self.summary = __summary__

    def __str__(self):
        return f"{__title__} {__summary__} version {__version__}"
