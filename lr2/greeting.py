#!/usr/bin/python3
import sys


class FormatError(Exception):
    pass


def greet(name):
    print(f"{name}, приятно познакомиться!")


def validate(name):
    if not all(char.isalpha() for char in name):
        raise FormatError(f"Ошибка: {name} - не является именем!")
    if name[0].islower():
        raise FormatError(f"Ошибка: {name} - имя должно начинаться с заглавной буквы!")


def process(line):
    names = line.split()
    for name in names:
        try:
            validate(name)
            greet(name)
        except FormatError as e:
            print(e, file=sys.stderr)


def main():
    is_term = sys.stdin.isatty()
    while True:
        if is_term:
            print("Привет, как тебя зовут?")
        try:
            line = sys.stdin.readline()
            if not line:
                break
            process(line)
        except KeyboardInterrupt:
            print("\nПока!")
            break


if __name__ == "__main__":
    main()
