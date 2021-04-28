from dataclasses import dataclass
from typing import Union
import json


@dataclass
class Event:
    REMOTE_HEIGHT = 'remote_height'
    QUIT = 'quit'
    REMOTE_BALL_COORDS = 'remote_ball_coords'

    type: str
    remote_height: Union[int, None] = None
    remote_width: Union[int, None] = None

    def to_line(self):
        return json.dumps({
            'type': self.type,
            'remote_height': self.remote_height,
            'remote_width': self.remote_width
        }).encode()

    @classmethod
    def from_line(cls, line):
        data = json.loads(line)
        return cls(**data)
