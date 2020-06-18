from dataclasses import dataclass
from network import Payload
from datetime import datetime
import time


@dataclass
class colors:
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class puts:
    @staticmethod
    def result(all_verdic: str, all_score: int, all_time: int):
        print(f"\t{colors.BOLD}", end="")
        for c in all_verdic:
            if c == "P":
                print(colors.GREEN, end="")
            elif c == "S":
                print(colors.YELLOW, end="")
            elif c == "X":
                print(colors.BLUE, end="")
            elif c == "T":
                print(colors.CYAN, end="")
            else:
                print(colors.RED, end="")
            print(c, end="")
        print(f"{colors.RESET} --> {all_score} pts.\n\ttook {all_time} ms.")

    @staticmethod
    def payload_info(payload: Payload):
        print(f"Timestamp\t: {datetime.fromtimestamp(payload.timestamp)}")
        print(f"User ID\t\t: {payload.user_id}")
        print(f"Problem ID\t: {payload.problem_id}")


class says:
    @staticmethod
    def kiyago(s: str):
        print(f"[ {colors.BOLD}{colors.WHITE}KIYAGO{colors.RESET} ] {s}")

    @staticmethod
    def err(s: str):
        print(f"[ {colors.BOLD}{colors.RED}ERROR{colors.RESET} ]  {s}")

    @staticmethod
    def ok(s: str):
        print(f"[ {colors.BOLD}{colors.GREEN}OK{colors.RESET} ]     {s}")

    @staticmethod
    def make(s: str):
        print(f"[ {colors.BOLD}{colors.BLUE}MAKE{colors.RESET} ]   {s}")
