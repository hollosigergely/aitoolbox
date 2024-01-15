import os
from abc import ABC, abstractmethod
from . import sources
from . import destinations

class Context(ABC):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = NotebookContext()

        return cls._instance
    
    @classmethod
    def set(cls,context):
        cls._instance = context

    @abstractmethod
    def get_sources(self):
        pass

    @abstractmethod
    def get_destinations(self):
        pass

    @abstractmethod
    def get_env(self, key):
        pass


class NotebookContext(Context):
    def __init__(self):
        self.sources = sources.TestSources()
        self.dest = destinations.TestDestination()
        self.env = {}

    def get_sources(self):
        return self.sources
    
    def get_destinations(self):
        return self.dest

    def get_env(self, key):
        return self.env[key]

    def set_env(self, key, value):
        self.env[key] = value
    

class ServerContext(Context):
    def __init__(self):
        self.sources = None
        self.dest = destinations.RESTDestination()

    def set_sources(self, sources):
        self.sources = sources

    def get_sources(self):
        return self.sources
    
    def get_destinations(self):
        return self.dest

    def get_env(self,key):
        return os.environ[key]