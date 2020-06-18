from dataclasses import dataclass


@dataclass
class Testcase:
    case_number: int = 0
    memory_limit: int = 256
    time_limit: int = 1000
    score: int = 10
