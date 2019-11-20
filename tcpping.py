import sys
import socket
import time
import argparse
from timeit import default_timer


def get_results(failed, passed):
    lRate = 0
    if failed != 0:
        lRate = failed / 4 * 100
        lRate = "%.2f" % lRate

    print(
        "\nTCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format(
            4, passed, failed, str(lRate)))


def start_ping(host, port):
    count = 0
    passed = 0
    failed = 0

    while count < 4:
        count += 1

        success = False

        s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(1)

        s_start = default_timer()

        try:
            s.connect((host, 80))
            s.shutdown(socket.SHUT_RD)
            success = True

        except socket.timeout:
            print("Connection timed out!")
            failed += 1
        except OSError as e:
            print("OS Error:", e)
            failed += 1

        s_stop = default_timer()

        s_runtime = "%.2f" % (1000 * (s_stop - s_start))

        if success:
            print("Reply from %s:%s: tcp_seq=%s time=%s ms" %
                  (host, port, count, s_runtime))
            passed += 1
            time.sleep(1)

    get_results(failed, passed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network utility TCPPING')
    parser.add_argument('host', type=str,
                        help='host to connect and send ping')
    parser.add_argument('port', type=int, nargs='?', default=80,
                        help='port of host')
    args = parser.parse_args()
    start_ping(args.host, args.port)
