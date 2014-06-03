import os
import sys
import re
import subprocess
import time
from TestingData import *

argv = sys.argv
default_regex = "tst_.*Test$"
input_format = "(--help | (--all | --fails) directory [regex])"

def my_print(str):
	print "# " + str.replace("\n", "\n# ")

def show_bad_input_message(message):
	my_print("%s See 'python %s --help'." % (message, argv[0]))
	my_print("The input format:")
	my_print(input_format)

def is_executable(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

if len(argv) == 2 and argv[1] == "--help":
	my_print("The script works with compiled Qt-tests located in a specified")
	my_print("directory and all its subdirectories.")
	my_print("It's designed for exluding manual execution of tests one by one")
	my_print("with searching for fails in the output.")
	my_print("Note that you still have to manually build all the tests.")
	my_print("")
	my_print("By default script runs all executables that match next regex: %s" % default_regex)
	my_print("But you can specify any other regular expression.")
	my_print("")
	my_print("The input must match next pattern:")
	my_print(input_format)
	exit()
elif len(argv) < 3:
	show_bad_input_message("Too few arguments.")
	exit()
elif len(argv) > 4:
	show_bad_input_message("Too many arguments.")
	exit()
elif argv[1] != "--all" and argv[1] != "--fails":
	show_bad_input_message("First argument is invalid: %s." % argv[1])
	exit()
elif os.path.isdir(argv[2]) == False:
	show_bad_input_message("Given path is not a directory: %s." % argv[2])
	exit()

displayed_info = argv[1]
directory = argv[2]
regex = argv[3] if len(argv) == 4 else default_regex

testing_data = TestingData()
for root, dirs, files in os.walk(directory):
	for file in files:
		match = re.match(regex, file)
		if (match):
			file_full_name = os.path.join(root, file)
			if is_executable(file_full_name):
				try:
					output = subprocess.check_output([file_full_name])
				except subprocess.CalledProcessError, e:
					output = e.output
				testing_data.on_test_executable_finished(output)
			else:
				my_print("Not executable (but matches regex): %s" % file)

if testing_data.is_empty == False:
	my_print("Executed %s group(s) of tests" % testing_data.executables_count)
	my_print("%s test(s) passed and %s test(s) failed." % (len(testing_data.passes), len(testing_data.fails)))
	my_print("Details:\n")
	if displayed_info == "--all":
		my_print(testing_data.entire_output)
	else:
		fails = testing_data.fails
		for fail in fails:
			my_print(fail.message)
else:
	show_bad_input_message("No tests are executed.\nDid you specify right directory and regular expression?")