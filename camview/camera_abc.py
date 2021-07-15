from enum import Enum
from abc import ABC, abstractmethod


class Resolution(Enum):
    A_REALLY_HIGH_RES = 1


class AbstractCam(ABC):
    @abstractmethod
    def open(self, res: Resolution, framerate=10):
        '''opens connection to camera and starts streaming'''
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass
 
    @abstractmethod
    def grab(self):
        '''returns next frame as numpy opencv image'''
        pass







