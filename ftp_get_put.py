# -*- coding:utf-8 -*-
# Author: Xin Li <xinii@msn.com>

import os
import sys
import base64

def main(task):
    argv = sys.argv
    argc = len(argv)
    if (argc != 2):
        print("FTP mput and mget")
        print("Usage: python %s <you file>" % argv[0])
        quit()
        
    path = os.path.expanduser("./ftp-script")
    tmp_ftp_file = "%s/tmp_ftp_file" % os.path.expanduser(".")
    with open("%s/pass" % path) as password:
        password = bytes.decode(base64.b64decode(password.readline()))
        password = password.split("\n")[0]
        with open("%s/ftp_script" % path) as ftp_file:
            lines = ftp_file.readlines()
            lines[1] = lines[1].replace("!!!", password)
            lines[3] = lines[3].replace("###", "m%s %s" % (task, argv[1]))
            with open (tmp_ftp_file, 'w', encoding='utf8') as output:
                output.writelines(lines)

    os.system("ftp -n < %s" % tmp_ftp_file)
    print("")
    os.remove(tmp_ftp_file)

if __name__ == "__main__":
    task = input("put(p) or get(g)? ")
    if(task == "p"):
        main("put")
    elif(task == "g"):
        main("get")
