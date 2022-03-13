import datetime
from abc import ABC, abstractmethod
import os
import subprocess
import re
class SUT(ABC):
    @abstractmethod
    def download(self, datetime_obj):
        pass

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def applyDepAnalysis(self):
        pass
