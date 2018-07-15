'''
Base class for singleton.
Class which needs to be singleton just inherits this one.
'''

# ref: https://stackoverflow.com/a/6798042/6247004


class Singleton:
    '''Base singleton class'''

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]
