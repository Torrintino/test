#!/usr/bin/python3

"""
Usage: ./valgrind_test.py ./test_case [-i input_file][-o output_file] args

This script will execute the given binary and report whether any memory
leaks or access errors occurred. It returns 0 on success and 1 if the
test failed. The output of valgrind will be written to log.txt

Arguments:
    -i input_file: input_file must be a path to a text file. It will be
        passed to the program via stdin.
    -o output: output_file must be a path to a text file. If it is set,
        the output of the program will be written to 'test_output'. If such
        file already exists in the working directory, it will be overwritten.
        'test_output' will be compared with the output_file and if they differ
        an error message will be printed. If the are equal, the 'test_output'
        file will be deleted.
    args: Any arguments at the end of the argument list will be passed as
        arguments to the test program.
"""

import os
import subprocess
import sys

input_file = None
input_path = None
output_file = None
output_path = None
args = []

if len(sys.argv) < 2:
    print("Invalid arguments")
    exit(1)
test_case = sys.argv[1]
    
skip = False
for i in range(2, len(sys.argv)):
    if skip:
        skip = False
        continue
    if sys.argv[i] == '-i':
        if input_file or (i == len(sys.argv) - 1) or args:
            print("Invalid arguments")
            exit(1)
        input_path = sys.argv[i + 1]
        skip = True
    elif sys.argv[i] == '-o':
        if output_file or (i == len(sys.argv) - 1) or args:
            print("Invalid arguments")
            exit(1)
        output_path = sys.argv[i + 1]
        skip = True
    else:
        args.append(sys.argv[i])

command = ["valgrind", "--error-exitcode=1", "--leak-check=full", test_case]
command += args

if input_path:
    input_file = open(input_path)
if output_path:
    expected_output_file = open(output_path, "r")
    output_file = open("test_output", "w")
log_file = open("log.txt", "w")

result = subprocess.call(command, stdin=input_file, stdout=output_file,
                         stderr=log_file)


if result:
    print("The test failed. You can find the output of valgrind in log.txt")
else:
    if output_path:
        result = subprocess.call(["diff", output_path, "test_output"])
        if result:
            print("The expected output differs from the actual output")
        else:
            print("Test succeeded")
    else:
        print("Test succeeded")

if input_path:
    input_file.close()
if output_path:
    expected_output_file.close()
    output_file.close()
log_file.close()

exit(result)
