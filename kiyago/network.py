import time
from dataclasses import dataclass


@dataclass
class Payload:
    timestamp: int = 0
    problem_id: int = 0
    user_id: int = 0


def get():
    return Payload(time.time(), 0, 0)
