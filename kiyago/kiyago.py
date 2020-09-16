#!/usr/bin/python3
from core import decor, make, utils,file_type
#import network
import Test_network as network
import yaml
import subprocess
import os
import time


# Communicate with judge.
def get_verdic(judge_path: str, prob_dir: str, at_case: int,lang:str,lang_bin:str) -> list:
    try:
        proc = subprocess.run([judge_path, prob_dir, at_case, lang,lang_bin], stdout=subprocess.PIPE)
        out = proc.stdout.decode("UTF-8").strip()
        result = out.split(";")
    except:
        result = ("!", 0, 0, "JUDGEER")

    if len(result) != 4 or result[3] not in [
        "OK",
        "UNSPECI",
        "TIMELXC",
        "MEMLXC",
        "FPEXCPT",
        "SEGMFLT",
        "ABORT",
        "JUDGEER",
    ]:
        result = ("!", 0, 0, "JUDGEER")
    
    if result[3] != "OK":
        decor.says.kiyago(f"At case {at_case} Got KSES : {result[3]}.")
    #        Verdic         Score           Time
    return (result[0], int(result[2]), int(result[1]))


# Parse meta-config from config.yaml
def get_init_kiyago_conf() -> dict:
    with open("./kiyago/config.yaml") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# Subtitute all placeholders in meta-config with the actual data
def get_kiyago_conf(init_conf) -> dict:
    _rep = (
        ("[PROBLEM_ID]", payload.problem_id),
        ("[USER_ID]", payload.user_id),
        ("[TIMESTAMP]", payload.timestamp),
    )
    kiyago_conf = {}    
    for k, v in init_conf.items():
        if type(v) == str:
            for rp, pd in _rep:
                v = v.replace(rp, str(pd))
        kiyago_conf[k] = v
    return kiyago_conf


# Parse problem's config.yaml
def get_problem_conf(problem_dir: str) -> dict:
    with open(f"{problem_dir}/config.yaml") as f:
        problem_conf = {k: v for k, v in yaml.load(f, Loader=yaml.FullLoader).items()}
    return problem_conf


def on_recieve():
    global kiyago_conf, problem_conf,payload
    decor.says.kiyago("Started compiling...")

    # Compile and check compile result
    make_ok = make.make(kiyago_conf, problem_conf,payload.lang)

    # If not make ok
    if not make_ok:
        decor.says.err("Cannot compile source file.")
        return None
    
    decor.says.ok("Source file compiled")

    if problem_conf["custom_judge"]:
        judge_path = problem_conf["judge_path"]
        decor.says.kiyago(f"This problem uses custom judge binary at :\n\t{judge_path}")
    else:
        judge_path = "./kiyago/bin/std_judge"

    # Verdic, score, elapse
    all_result = ["", 0, 0]

    decor.says.kiyago("Started grading...")

    # Get verdic for each testcase
    for i in range(1, problem_conf["n_cases"] + 1):
        result = get_verdic(judge_path, kiyago_conf["problem_dir"], str(i),payload.lang,kiyago_conf["subject_bin"])
        for i in range(3):
            all_result[i] += result[i]
    
    # Display result
    decor.says.ok("Finished grading : ")
    decor.puts.result(*all_result)

    # Delete subject's binary
    if os.path.exists(kiyago_conf['subject_bin']):
        os.system(f"rm {kiyago_conf['subject_bin']}")
        decor.says.ok("Binary deleted.")

    # Move subject's source to archives/
    if not os.path.exists(kiyago_conf["archive_dir"]):
        utils.mkdir_rcv(kiyago_conf["archive_dir"])
    os.system(f"mv {kiyago_conf['subject_src']} {kiyago_conf['archive_dir']}")
    decor.says.ok(f"Source code archived at : {kiyago_conf['archive_dir']}")
    return all_result


# Entry
if __name__ == "__main__":
    decor.says.kiyago("Grader started. Waiting for submission...")

    # Get meta-config
    init_kiyago_conf = get_init_kiyago_conf()

    # Establish connection to DB.
    try:
        db_connector = network.Network()
    except:
        decor.says.err("Cannot establish connection to database.")
        exit(0)

    # Main loop
    while True:
        # Try to fetch new query
        payload = db_connector.get()
        if payload != None:
            print("PAYLOAD ------------------------------------")
            decor.puts.payload_info(payload)
            
            # Get config files accordingly
            # Subtitute placeholders
            kiyago_conf = get_kiyago_conf(init_kiyago_conf)
            problem_conf = get_problem_conf(kiyago_conf["problem_dir"])
            
            kiyago_conf["subject_src"] += file_type.langsrc2filetype(payload.lang)
            kiyago_conf["archive_dir"] += file_type.langsrc2filetype(payload.lang)
            kiyago_conf["subject_bin"] += file_type.langbin2filetype(payload.lang)

            #print("Meow",kiyago_conf["subject_src"])

            # Write subject source file.
            utils.write_file(kiyago_conf["subject_src"], payload.code)

            # Compile and judge; None = compile error
            result = on_recieve()

            if result == None:
                print("ERRMSG -------------------------------------")
                # Show error message
                with open(
                    f"{kiyago_conf['cmp_err']}"
                ) as f:
                    errmsg = f.read()
                print(errmsg)
                db_connector.send_error(errmsg)
            else:
                db_connector.send_result(result)
            print("--------------------------------------------")
            decor.says.kiyago("Finished grading. Waiting for the next session.")

        db_connector.update()
        time.sleep(init_kiyago_conf["sleep_interval"])
