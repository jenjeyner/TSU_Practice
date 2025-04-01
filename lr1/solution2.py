#!/usr/bin/python3

import random
import sys


def addToLog(message):
    file = "log2.txt"
    with open(file, "a") as log:
        log.write(message)


def main():
    try:
        prev_int = int(sys.stdin.read().strip())
        rnd_int = random.randint(-10, 10)
        addToLog(f"Прошлое число: {prev_int}, новое число: {rnd_int}\n")
        res_div = prev_int / rnd_int
    except ZeroDivisionError:
        print("Ошибка: деление на 0\n", file=sys.stderr)
        addToLog("Ошибка: деление на 0\n")
    else:
        addToLog(f"Результат деления: {res_div}\n")
        print(res_div, file=sys.stdout)


if __name__ == "__main__":
    main()
