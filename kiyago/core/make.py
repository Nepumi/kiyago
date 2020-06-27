from network import Payload
from core import decor, utils
import yaml
import os


def get_make_cmd(kiyago_conf: dict, problem_conf: dict) -> str:
    phd = ["[PROBLEM_DIR]", "[GRADER_DEFINE]", "[SRC_PATH]", "[BIN_PATH]"]
    rep = [
        kiyago_conf["problem_dir"],
        kiyago_conf["grader_define"],
        kiyago_conf["subject_src"],
        kiyago_conf["subject_bin"],
    ]
    for i in range(len(phd)):
        problem_conf["compile"] = problem_conf["compile"].replace(phd[i], str(rep[i]))

    if not os.path.exists(kiyago_conf['cmp_out']):
        utils.mkdir_rcv(kiyago_conf['cmp_out'])

    if not os.path.exists(kiyago_conf['cmp_err']):
        utils.mkdir_rcv(kiyago_conf['cmp_err'])

    IOREDIRECT = f"1>{kiyago_conf['cmp_out']} 2>{kiyago_conf['cmp_err']}"
    return f"{problem_conf['compile']} {IOREDIRECT}"


def make(kiyago_conf: dict, problem_conf: dict):
    make_cmd = get_make_cmd(kiyago_conf, problem_conf)
    decor.says.make(f"Make command : {make_cmd}")

    os.system(make_cmd)

    if os.path.exists(kiyago_conf['subject_bin']):
        return True
    else:
        return False
