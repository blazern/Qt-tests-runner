qt-tests-runner
==============

The script works with compiled Qt-tests located in a specified directory and all its subdirectories.
It's designed for exluding manual execution of tests one by one with searching for fails in the output.
Note that you still have to manually build all the tests.

By default script runs all executables that match next regex: tst_.*Test$
But you can specify any other regular expression.

The input must match next pattern:
(--help | (--all | --fails) directory [regex])
