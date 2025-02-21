#  How to test the code

For verifying the functionality of the python code, first install [pytest](https://docs.pytest.org/en/6.2.x/) via

    pip install -U pytest

Note: If you install pytest inside a virtual environment, you have to deactivate and then reactivate the environment for pytest to be used in the virtual environment.
Every trajectory optimization algorithm and every controller in this software package has a unit_test.py file which verfies the functionality of the corresponding piece of software. The pendulum plant has a unit_test.py script as well.

pytest automatically identifies all python scripts with names "\*\_test.py" or "test\_\*.py" in the current directory and all subdirectories. Therefore, if you want to perform all unit tests in this software package, simply go to the [python root directory](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/tree/master/software/python) and type

    python -m pytest

If you want perform a specific unit test (e.g. for the lqr controller) use

    pytest software/python/controller/lqr/unit_test.py




