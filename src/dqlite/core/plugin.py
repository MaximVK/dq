from abc import ABC, abstractmethod


class BasePlugin(ABC):
    @property
    @abstractmethod
    def adapter_class(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def environment_class(self):
        raise NotImplementedError
