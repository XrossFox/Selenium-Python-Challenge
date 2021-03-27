# Selenium-Python-Challenge
Selenium and python, test automation challenge.

Instructions, how to use this thing:
- install the following python 3 dependencies: `selenium`

- run tests with unittest: `py -m unittest tests.test_selenium`. Make sure you are in the directory that contains the `tests` directory. If you cant see it, you are in the wrong place.

- - Note: the testrunner looks for the gecko driver in the driver directory, it will most likely not work on any OS that is not windows.

## Why the automation is done in a single test case?
Because unittest doesn't allow to keep state between test cases easily. Because it also messes up test case order by sorting by whatever the heck it pleases, and making it to run the test cases in the proper order is not so tribial as it might seem, at least not without resorting to weird naming conventions. But is mostly becuase unittest doesn't expect you to persist state between test cases and makes things a bit harder.
