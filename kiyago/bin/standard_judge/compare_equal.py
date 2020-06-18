def compare_equal(res_path, sol_path):
    with open(res_path) as in_file, open(sol_path) as sol_file:
        while True:
            try:
                in_line = in_file.readline()
                sol_line = sol_file.readline()
            except:
                return False

            if in_line == "" and sol_line == "":
                return True

            if sol_line.split() != in_line.split():
                return False
