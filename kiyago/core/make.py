from network import Payload
from core import decor
import yaml
import os


def get_make_cmd(kiyago_conf: dict, problem_conf: dict) -> str:
    phd = ["[PROBLEM_DIR]", "[GRADER_DEFINE]", "[SRC_NAME]", "[BIN_NAME]"]
    rep = [
        kiyago_conf["problem_dir"],
        kiyago_conf["grader_define"],
        kiyago_conf["subject_src"],
        kiyago_conf["subject_bin"],
    ]
    for i in range(len(phd)):
        problem_conf["compile"] = problem_conf["compile"].replace(phd[i], str(rep[i]))

    IOREDIRECT = f"1>{kiyago_conf['problem_dir']}/{kiyago_conf['cmp_out']} 2>{kiyago_conf['problem_dir']}/{kiyago_conf['cmp_err']}"
    return f"{problem_conf['compile']} {IOREDIRECT}"


def make(kiyago_conf: dict, problem_conf: dict):
    make_cmd = get_make_cmd(kiyago_conf, problem_conf)
    decor.says.make(f"Compiling with command : {make_cmd} ")

    # TODO add try catch

    os.system(make_cmd)

    bin_path = f"{kiyago_conf['problem_dir']}/{kiyago_conf['subject_bin']}"

    if os.path.exists(bin_path):
        decor.says.ok("Source file compiled")
        return True
    else:
        decor.says.err("Cannot compile source file.")
        return False
