import os
import time
import subprocess
import signal
from .Testcase import Testcase


def execute(case: Testcase, judge_conf: dict) -> (int, str):  # (elapsed, kses)
    tmp_path = judge_conf["tmp_path"]
    if not os.path.exists(tmp_path):
        os.system(f"mkdir {tmp_path}")

    try:
        exec_path = judge_conf["exec_path"]
        in_path = judge_conf["in_path"]
        out_path = judge_conf["out_path"]
        err_path = judge_conf["err_path"]
        mem_limit_kb = case.memory_limit * 1024
    except:
        return 0, "JUDGEER"

    run_command = f"ulimit -v {mem_limit_kb}; {exec_path} 0<{in_path} 1>{out_path} 2>{err_path}; exit;"

    start_time = time.time()
    proc = subprocess.Popen([run_command], shell=True, preexec_fn=os.setsid)
    try:
        proc.communicate(timeout=case.time_limit)
        t = proc.returncode
    except subprocess.TimeoutExpired:
        t = 124  # TLE

    elapsed = time.time() - start_time

    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    ts = [0, 124, 134, 136, 139]
    KSES = ["OK", "TIMELXC", "ABORT", "FPEXCPT", "SEGMFLT"]
    try:
        kses = KSES[ts.index(t)]
    except ValueError:
        kses = "UNSPECI"

    return int(elapsed * 1000), kses
