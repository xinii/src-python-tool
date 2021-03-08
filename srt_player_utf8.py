# -*- coding:utf-8 -*-
# Author: Xin Li <xinii@msn.com>

import os
import time
import sys
from datetime import datetime

def output(msg):
    os.system('echo "' + str(msg) + '" | lolcat')

def only_for_omobana(i):
    array = ['Ionian', 'Dorian', 'Aeolian', 'Phrygian', 'Lydian', 'Mixolydian', 'Locrian']
    os.system('figlet "' + array[i] + '"')

def main():
    argv = sys.argv
    argc = len(argv)
    if (argc != 2):
        #引数がちゃんとあるかチェック
        #正しくなければメッセージを出力して終了
        print('Usage: python %s <you file>.srt' % argv[0])
        quit()

    path = './%s' % argv[1]
    zero = datetime.strptime('00:00:00,000', '%H:%M:%S,%f')

    with open(path) as fp:
        lines = fp.read().split('\n\n')

    for i in range(len(lines)):
        current_item = lines[i].split('\n')
        if(len(current_item) == 3):
            time_now = current_item[1].split(' --> ')
            a = datetime.strptime(time_now[0], '%H:%M:%S,%f')
            b = datetime.strptime(time_now[1], '%H:%M:%S,%f')
            zero = a - zero
            c = b - a
            if(zero.total_seconds() > 0):
                time.sleep(zero.total_seconds())
            else:
                c = c + zero

            zero = b
            # print('%s %s' % (current_item[2], current_item[1]))
            if(i < 7):
                only_for_omobana(i)

            output(current_item[2])
            # output(current_item[1])
            if(c.total_seconds() > 0):
                time.sleep(c.total_seconds())

            output('~~~')


if __name__ == '__main__':
    # a = datetime.strptime('30/03/09 16:31:32.123', '%d/%m/%y %H:%M:%S.%f')
    # now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    main()
