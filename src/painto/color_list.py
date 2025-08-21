from .color import Color
import random

class ColorList(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
    
    def random(self, count: int = 1) -> Color:
        return random.sample(list(self.values()), count)
