import logging
from abc import ABC, abstractmethod
from typing import ClassVar

from ModuBotCore import BaseConfig


class BaseModule(ABC, BaseConfig):
    """
    Abstract base class for all ModuBot modules.

    All modules must inherit from this class and implement the `on_enable` and `on_disable` lifecycle methods.

    :cvar NAME: The name of the module.
    :cvar ENABLING: Whether this module should be loaded and enabled.
    """

    NAME: ClassVar[str] = "BaseModule"
    ENABLING: ClassVar[bool] = True

    @property
    def logger(self) -> logging.Logger:
        """
        Returns a logger instance specific to the module.

        :return: Logger named after the module.
        :rtype: logging.Logger
        """
        return logging.getLogger(self.NAME)

    @abstractmethod
    def on_enable(self):
        """
        Hook that is called when the module is enabled.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def on_disable(self):
        """
        Hook that is called when the module is disabled.
        Must be implemented by subclasses.
        """
        pass
