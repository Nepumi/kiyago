#!/usr/bin/python3
from core import decor, make
import network
import yaml
import subprocess
import os


def send_cmp_error():
    with open(f"{kiyago_conf['problem_dir']}/{kiyago_conf['cmp_err']}") as f:
        print(f.read())
        # TODO send to mySQL


def send_result(result: tuple):
    pass


def get_verdic(judge_path: str, prob_dir: str, at_case: int) -> list:
    proc = subprocess.run([judge_path, prob_dir, at_case], stdout=subprocess.PIPE)
    out = proc.stdout.decode("UTF-8").strip()
    result = out.split(";")
    if result[3] != "OK":
        decor.says.kiyago(f"Got KSES : {result[3]} at case {at_case}.")
    return (result[0], int(result[2]), int(result[1]))


def get_kiyago_conf(payload: network.Payload) -> dict:
    _rep = (
        ("[PROBLEM_ID]", payload.problem_id),
        ("[USER_ID]", payload.user_id),
        ("[TIMESTAMP]", payload.timestamp),
    )
    with open("./kiyago/config.yaml") as f:
        kiyago_conf = {}
        for k, v in yaml.load(f, Loader=yaml.FullLoader).items():
            _v = v
            for rp, pd in _rep:
                _v = _v.replace(rp, str(pd))
            kiyago_conf[k] = _v

    return kiyago_conf


def get_problem_conf(problem_dir: str) -> dict:
    with open(f"{problem_dir}/config.yaml") as f:
        problem_conf = {k: v for k, v in yaml.load(f, Loader=yaml.FullLoader).items()}
    return problem_conf


def on_recieve():
    global kiyago_conf, problem_conf
    print("\t--> Compiling")

    # Compile and check result
    make_ok = make.make(kiyago_conf, problem_conf)

    if not make_ok:
        return None

    if problem_conf["custom_judge"]:
        judge_path = problem_conf["judge_path"]
    else:
        judge_path = "./kiyago/bin/std_judge"

    all_verdic = ""
    all_score = 0
    all_time = 0

    for i in range(1, problem_conf["n_cases"] + 1):
        result = get_verdic(judge_path, kiyago_conf["problem_dir"], str(i))
        all_verdic += result[0]
        all_score += result[1]
        all_time += result[2]


    decor.says.kiyago("Finished grading : ")
    decor.puts.result(all_verdic, all_score, all_time)

    # Delete subject's binary
    bin_path = f"{kiyago_conf['problem_dir']}/{kiyago_conf['subject_bin']}"
    if os.path.exists(bin_path):
        os.system(f"rm {bin_path}")
    decor.says.ok("Binary deleted.")

    # Move subject's source to archives
    arch_path = f"{kiyago_conf['problem_dir']}/compile_space/{kiyago_conf['subject_src']}"
    if os.path.exists(arch_path):
        os.system(f"mv {arch_path} {kiyago_conf['archive_dir']}")
    decor.says.ok(f"Source code archived at\n\t--> {kiyago_conf['archive_dir']}")
    return (all_verdic, all_score, all_time)


decor.says.kiyago("Grader started. Waiting for submission...")
##############################
# TODO : Add network traffic #
##############################
decor.says.ok("Payload received.")
payload = network.get()

print("--------------------------------------------")
decor.puts.payload_info(payload)
kiyago_conf = get_kiyago_conf(payload)
problem_conf = get_problem_conf(kiyago_conf["problem_dir"])

result = on_recieve()

if result == None:
    print("--------------------------------------------")
    send_cmp_error()
else:
    send_result(result)
print("--------------------------------------------")
