# -*- coding:utf-8 -*-
# Author: Xin Li <xinii@msn.com>

import subprocess

path = subprocess.getoutput("echo $PATH")
path = path.split(":")
for i in range(len(path)):
    print("[%i] %s" % (i, path[i]))
