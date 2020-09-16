from network import Payload
from core import decor, utils
import yaml
import os


def get_make_cmd(kiyago_conf: dict, problem_conf: dict,lang:str) -> str:
    phd = ["[PROBLEM_DIR]", "[GRADER_DEFINE]", "[SRC_PATH]", "[BIN_PATH]","[CMP_OUT]","[CMP_ERR]"]
    rep = [
        kiyago_conf["problem_dir"],
        kiyago_conf["grader_define"],
        kiyago_conf["subject_src"],
        kiyago_conf["subject_bin"],
        f"1>{kiyago_conf['cmp_out']}",
        f"2>{kiyago_conf['cmp_err']}",
    ]
    for i in range(len(phd)):
        problem_conf["compile"][lang] = problem_conf["compile"][lang].replace(phd[i], str(rep[i]))

    if not os.path.exists(kiyago_conf['cmp_out']):
        utils.mkdir_rcv(kiyago_conf['cmp_out'])

    if not os.path.exists(kiyago_conf['cmp_err']):
        utils.mkdir_rcv(kiyago_conf['cmp_err'])

    return f"{problem_conf['compile'][lang]}"


def make(kiyago_conf: dict, problem_conf: dict,lang:str):
    make_cmd = get_make_cmd(kiyago_conf, problem_conf,lang)
    decor.says.make(f"Make command : {make_cmd}")

    os.system(make_cmd)

    if os.path.exists(kiyago_conf['subject_bin']):
        return True
    else:
        return False
