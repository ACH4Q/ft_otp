import argparse
import os
import time

def main():
    parser = argparse.ArgumentParser(description="ft_otp")
    parser.add_argument("-g",
                        "--generate",
                        metavar="KEY_FILE",
                        help="ft")
    parser.add_argument("-k",
                        "--key",
                        metavar="KEY_FILE",
                        help="ft")
    args = parser.parse_args()
    current_time = int(time.time())
    TIME_STEP = 30
    T = current_time / TIME_STEP

    print("chi haja")
    print(current_time)
    print(T)


if (__name__ == "__main__"):
    main()