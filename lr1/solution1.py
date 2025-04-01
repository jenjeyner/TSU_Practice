#!/usr/bin/python3

import random
import sys


def addToLog(message):
    file = "log1.txt"
    with open(file, "a") as log:
        log.write(message)


def main():
    rnd_int = random.randint(-10, 10)
    addToLog(f"Случайное число: {rnd_int}\n")
    print(rnd_int, file=sys.stdout)


if __name__ == "__main__":
    main()
