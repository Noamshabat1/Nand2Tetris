# AUTHOR danielnachumdev
import subprocess
from danielutils import acm, get_directories, ColoredText, get_files, get_file_type_from_directory, create_directory, is_directory, file_exists, delete_directory, is_file
from LOCALS import LOCAL_COMPILER
from pathlib import Path
import os
STATUS_OK = 0

# ==============================================  CHANGE STUFF HERE   ==============================================
BUILTIN_COMPILER_PATH = LOCAL_COMPILER
PRETTY_PRINT_THE_RESULT = True
RECOMPILE_COMPARE_FILES_WITH_BUILTIN_COMPILER = True
TESTS_FOLDER = "./tests"
DISPLAY_ONLY_FAILS = True
HOW_MANY_ERRORS_TO_SHOW_PER_FILE = 1
# ==============================================  END OF CHANGE AREA   =============================================


def move_file(old_path: str, new_path: str) -> None:
    os.rename(old_path, new_path)


def create_compare_files(test):
    def cm(*args, shell: bool = True):
        if not isinstance(shell, bool):
            raise TypeError(
                "In function 'cm' param 'shell' must be of type bool")
        if Path(args[0]).is_file():
            args = (f"\"{args[0]}\"", *args[1:])
        res = subprocess.run(" ".join(args), shell=shell, capture_output=True)
        return res.returncode, res.stdout, res.stderr

    return_code, stdout, stderr = cm(
        BUILTIN_COMPILER_PATH, f"{TESTS_FOLDER}/{test}")
    if return_code != 0:
        print("problem with builtin compiler")
        exit(0)
    else:
        vm_files = get_file_type_from_directory(
            f"{TESTS_FOLDER}/{test}", ".vm")
        if is_directory(f"{TESTS_FOLDER}/{test}/cmp"):
            delete_directory(f"{TESTS_FOLDER}/{test}/cmp/")
        create_directory(f"{TESTS_FOLDER}/{test}/cmp")
        for file in vm_files:
            new_name = Path(f"{TESTS_FOLDER}/{test}/{file}").stem+f".tst.vm"
            if not file_exists(f"{TESTS_FOLDER}/{test}/cmp/{new_name}"):
                move_file(f"{TESTS_FOLDER}/{test}/{file}",
                          f"{TESTS_FOLDER}/{test}/cmp/{new_name}")


def create_files(test):
    print(f"Compiling {test}: ", end="")
    return_code, stdout, stderr = acm(
        f"python ./JackCompiler.py {TESTS_FOLDER}/{test}", [], 0.1, shell=False)
    if return_code != 0:
        msg = "FAIL "
        if PRETTY_PRINT_THE_RESULT:
            msg = ColoredText.red(msg)
        print(msg)
    else:
        msg = "PASS "
        if PRETTY_PRINT_THE_RESULT:
            msg = ColoredText.green(msg)
        print(msg)
    return return_code


def compare(test):
    res_files = set([file for file in get_files(
                    f"{TESTS_FOLDER}/{test}/") if Path(file).suffix == ".vm"])
    cmp_files = set([file for file in get_files(
        f"{TESTS_FOLDER}/{test}/cmp/") if Path(file).suffix == ".vm"])
    dic = {key: value for key, value in [
        (f"{file.split('.')[0]}.vm", file) for file in cmp_files]}
    for file in res_files:

        with open(f"{TESTS_FOLDER}/{test}/{file}", "r") as res:
            with open(f"{TESTS_FOLDER}/{test}/cmp/{dic[file]}", "r") as cmp:
                res_lines = res.readlines()
                cmp_lines = cmp.readlines()
                l = min(len(res_lines), len(cmp_lines))
                i = 0
                buffer = []
                while (i < l):
                    if (res_lines[i] != cmp_lines[i]):
                        buffer.append(
                            f"Difference found on line {i+1}")
                    i += 1
                if (len(buffer) > 0 or len(res_lines) != len(cmp_lines)):
                    msg = "FAIL "
                    if PRETTY_PRINT_THE_RESULT:
                        msg = ColoredText.red(msg)
                    print(f"\t{file} diff: ", end="")
                    print(msg)
                    for diff in buffer[:HOW_MANY_ERRORS_TO_SHOW_PER_FILE]:
                        print(f"\t\t{diff}")
                else:
                    if not DISPLAY_ONLY_FAILS:
                        msg = "PASS "
                        if PRETTY_PRINT_THE_RESULT:
                            msg = ColoredText.green(msg)
                        print(f"\t{file} diff: ", end="")
                        print(msg)


def main():
    assert HOW_MANY_ERRORS_TO_SHOW_PER_FILE >= 1, "ERROR_DISPLAY_LENGTH must be at least 1"
    tests = get_directories(TESTS_FOLDER)
    for test in tests:
        try:
            create_compare_files(test)
            if create_files(test) == STATUS_OK:
                compare(test)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    if not is_file(BUILTIN_COMPILER_PATH):
        print("can't find builtin compiler")
    else:
        main()
