import time
from quickprofile import profile_time, profile_block, profile_line


def test_example_function():
    @profile_time
    def dummy_function():
        time.sleep(1)

    dummy_function()


def test_block_profiling():
    with profile_block():
        time.sleep(0.5)


def test_line_profiling():
    with profile_line():
        total = sum(i for i in range(1000))
