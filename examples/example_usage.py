from quickprofile import profile_time, profile_block, profile_line
import time

@profile_time
def example_function():
    time.sleep(2)  # Simulating a time-consuming task

def main():
    example_function()

    with profile_block():
        time.sleep(1)  # Simulating another time-consuming task

    with profile_line():
        # Simulating some code that you want to profile specifically
        total = sum(i ** 2 for i in range(10**6))

if __name__ == "__main__":
    main()
