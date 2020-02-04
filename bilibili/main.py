#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
from pyfiglet import figlet_format

from bilibili.bilibili import get_analysis


def main():
    cookie_file = 'Cookies'
    print(figlet_format('bai piao', font='slant'))
    get_analysis(cookie_file)


if __name__ == '__main__':
    main()
