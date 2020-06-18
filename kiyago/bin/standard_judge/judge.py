#!/bin/python3

import sys
import yaml
import os

from .Testcase import Testcase
from .compare_equal import compare_equal
from .execute import execute

problem_path = sys.argv[1]
at_case = sys.argv[2]


def main():
    with open("./kiyago/bin/standard_judge/config.yaml") as f:
        judge_conf = {
            k: v.replace("[PROBLEM_DIR]", problem_path).replace("[#]", at_case)
            for k, v in yaml.load(f, Loader=yaml.FullLoader).items()
        }

    with open(judge_conf["cnf_path"]) as f:
        prob_conf = yaml.load(f, Loader=yaml.FullLoader)

    case = Testcase(
        case_number=int(at_case),
        memory_limit=prob_conf["memory_limit"],
        time_limit=prob_conf["time_limit"],
        score=prob_conf["case_score"],
    )

    elapsed, kses = execute(case, judge_conf)

    score = 0
    if kses == "OK":
        res = compare_equal(judge_conf["out_path"], judge_conf["sol_path"])
        verdic = "P" if res else "-"
        score = prob_conf["case_score"] if res else 0
    elif kses == "JUDGEER":
        verdic = "!"
    elif kses == "TIMELXC":
        verdic = "T"
    else:
        verdic = "X"

    # Clean up tmp directory
    os.system(f"rm -r {judge_conf['tmp_path']}")

    print(f"{verdic};{elapsed};{score};{kses}")
