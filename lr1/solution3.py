#!/usr/bin/python3

import sys


class NegativeError(Exception):
    pass


def addToLog(message):
    file = "log3.txt"
    with open(file, "a") as log:
        log.write(message)


def main():
    try:
        prev_num = float(sys.stdin.read().strip())
        addToLog(f"Прошлое число: {prev_num}\n")
        if prev_num < 0:
            raise NegativeError
    except ValueError:
        print("Поступившие данные не удалось привести к типу float\n", file=sys.stderr)
        addToLog("Поступившие данные не удалось привести к типу float\n")
    except NegativeError:
        print("Нельзя брать корень отрицательного числа\n", file=sys.stderr)
        addToLog("Нельзя брать корень отрицательного числа\n")
    else:
        res_sqr = prev_num ** (1/2)
        addToLog(f"Корень числа: {res_sqr}\n")
        print(res_sqr, file=sys.stdout)


if __name__ == "__main__":
    main()
