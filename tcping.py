import argparse
from modules.TCPing import TCPing


def parse(hosts_ports):
    res = []
    for e in hosts_ports:
        host, port = e.split(":")
        res.append((host, int(port)))
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tcping')
    parser.add_argument('host_port', nargs='*', type=str, metavar="host:port",
                        default=['localhost:1234'],
                        help='')
    parser.add_argument('--count', '-c', metavar='N', type=int, default=5,
                        help='')
    parser.add_argument('--timeout', '-t', metavar='N', type=int, default=3,
                        help='')
    parser.add_argument('--interval', '-i', metavar='N', type=int, default=1,
                        help='')
    args = parser.parse_args()
    hosts_ports = parse(args.host_port)
    for host, port in hosts_ports:
        TCPing(print, host, port, args.count, args.timeout, args.interval)
