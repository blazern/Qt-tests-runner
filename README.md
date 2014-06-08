Qt-tests-runner
==============

To run the script you need to have a Python interpreter installed on your system.

The script works with compiled Qt-tests located in a specified directory and all its subdirectories.
It's designed for excluding manual execution of tests one by one with searching for fails in the output.
Note that you still have to manually build all the tests.

The script runs all executables that match given regular expression.
If no regular expression is given then the script uses the default one: tst_.*Test$

Your input must match next pattern: (--help | directory (--all | --fails) [regex])

Also note that if the executables need some libraries to be added to your system's path variable, you would need to add them manually.
To do that on Linux execute: "export PATH=$PATH:path/to/needed/libraries".
To do that on Windows execute: "set Path=%Path%;path/to/needed/libraries".