import argparse
from modules.TCPing import TCPing
from modules.window import Screen
from threading import Thread
import yaml
from math import inf
import signal
import sys


def signal_handler(sig, frame):
    sys.exit(0)


def start():
    conf = yaml.safe_load(args.file_yaml)
    tcpings = []
    for e in conf:
        tcpings.append(TCPing(e['host'],
                              e['ports'],
                              args.count,
                              e['timeout'],
                              e['interval']))
    t = []
    for e in tcpings:
        t.append(Thread(target=e.start, daemon=True))
    signal.signal(signal.SIGINT, signal_handler)
    try:
        for e in t:
            e.start()
        Screen(tcpings)
        for e in t:
            e.join()
    except Exception as ex:
        print(str(ex), file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tcping')
    parser.add_argument('file_yaml', type=open,
                        help='')
    parser.add_argument('--count', type=int, metavar='N', default=inf,
                        help='')
    args = parser.parse_args()
    start()
