import os


def mkdir_rcv(path: str):
    lst = path.split("/")
    for i in range(1, len(lst) - 1):
        cur = f"{'/'.join(lst[:i+1])}"
        if not os.path.exists(cur):
            os.system(f"mkdir {cur}")


def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)
