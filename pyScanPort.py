#运行参数  python 脚本.py ip port-port
import sys
import _thread
from socket import *


def testPort(port):
    sock = socket(AF_INET,SOCK_STREAM)
    sock.settimeout(15)
    res = sock.connect_ex(target_ip,port)
    if res == 0:
        lock.acquire()
        print("{}开放/n".format(port))
        lock.release()
    else:
        print("未开放")
if __name__ == '__main__':
    hostname = sys.argv[1]
    portstrs = sys.argv[2].split('-')
    start_port = int(portstrs[0])
    end_port = int(portstrs[1])
    target_ip = gethostbyname(hostname)
    lock = _thread.allocate_lock()
    for port in range(start_port,end_port):
        _thread.start_new_thread(testPort,(port,))