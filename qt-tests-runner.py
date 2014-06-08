import os
import sys
import re
import subprocess
import time
from TestingData import *

argv = sys.argv
default_regex = "tst_.*Test$"
input_format = "(--help | directory (--all | --fails) [regex])"

def my_print(str):
	print "# " + str.replace("\n", "\n# ")

def show_bad_input_message(message):
	my_print("%s See 'python %s --help'." % (message, argv[0]))
	my_print("The input format:")
	my_print(input_format)

def is_executable(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

if len(argv) == 2 and argv[1] == "--help":
	my_print("The script works with compiled Qt-tests located in a specified \
directory and all its subdirectories.")
	my_print("It's designed for excluding manual execution of tests one by one \
with searching for fails in the output.")
	my_print("Note that you still have to manually build all the tests.")
	my_print("")
	my_print("The script runs all executables that match given regular expression.")
	my_print("If no regular expression is given then the script uses the default one: %s" % default_regex)
	my_print("")
	my_print("Your input must match next pattern:")
	my_print(input_format)
	my_print("")
	my_print("Also note that if the executables need some libraries to be added to \
your system's path variable, you would need to add them manually.")
	my_print("To do that on Linux execute: \"export PATH=$PATH:path/to/needed/libraries\".")
	my_print("To do that on Windows execute: \"set Path=%Path%;path/to/needed/libraries\".")
	exit()
elif len(argv) < 3:
	show_bad_input_message("Too few arguments.")
	exit()
elif len(argv) > 4:
	show_bad_input_message("Too many arguments.")
	exit()
elif argv[2] != "--all" and argv[2] != "--fails":
	show_bad_input_message("Displayed-info argument is invalid: %s." % argv[2])
	exit()
elif os.path.isdir(argv[1]) == False:
	show_bad_input_message("Given path is not a directory: %s." % argv[1])
	exit()

directory = argv[1]
displayed_info = argv[2]
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
	if displayed_info == "--all":
		entire_output = testing_data.entire_output
		if len(entire_output) > 0:
			my_print("Details:\n")
			my_print(testing_data.entire_output)
	else:
		fails = testing_data.fails
		if len(fails) > 0:
			my_print("Details:\n")
			for fail in fails:
				my_print(fail.message)
else:
	show_bad_input_message("No tests are executed.\nDid you specify right directory and regular expression?")