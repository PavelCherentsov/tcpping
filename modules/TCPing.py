import socket
from .Packet import Packet
from time import sleep, perf_counter
from math import inf
from enum import Enum
from threading import Thread


class Struct:
    def __init__(self, host, ports, timeout, interval):
        self.host = host
        self.ports = ports
        self.timeout = timeout
        self.interval = interval


class Flag(Enum):
    OPEN = 0,
    CLOSE = 1,
    NO_ANSWER = 2


class TCPing:
    def __init__(self, dest_ip, dest_port, count, timeout, interval):

        self.output = ["", "", "", ""]
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.count = count
        self.accept_count = 0
        self.timeout = timeout
        self.interval = interval

        self.total_time = 0
        self.min_time = inf
        self.max_time = 0

        self.p = Packet(socket.gethostbyname(dest_ip), self.dest_port)
        self.packet = self.p.generate_packet()
        self.c = 0

    def ping(self):
        s_start = perf_counter()
        try:
            self.send_packet(self.packet)
            syn_ack, len_data = self.recv_packet()
        except Exception:
            pass
        else:
            s_stop = perf_counter()

            time = round(1000 * (s_stop - s_start), 2)

            self.total_time += time
            self.min_time = min(self.min_time, time)
            self.max_time = max(self.max_time, time)
            self.avg_time = round(self.total_time / (self.c + 1), 2)

            self.print_packet(syn_ack, len_data, time)

    def start(self):
        self.output = [f"{self.dest_ip}:{self.dest_port}", "-", "-", "0/0/0"]
        pings = []
        self.c = 0
        while self.c < self.count:
            pings.append(Thread(target=self.ping, daemon=True))
            pings[self.c].start()
            sleep(self.interval)
            self.c += 1

        for i in range(self.count):
            pings[i].join()

        self.print_stat()

    def send_packet(self, packet):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                               socket.IPPROTO_TCP)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.s.settimeout(self.timeout)
        self.s.sendto(packet, (self.dest_ip, 0))

    def recv_packet(self):
        while True:
            try:
                data = self.s.recv(1024)
            except socket.timeout:
                res = Flag.NO_ANSWER, 0
                break
            if (Packet.get_scr_ip(data), Packet.get_dept_ip(data)) == (
                    Packet.get_dept_ip(self.packet),
                    Packet.get_scr_ip(self.packet)):
                if Packet.get_flag(data) == Packet.TCP_SYN_ACK:
                    self.accept_count += 1
                    res = Flag.OPEN, len(data)
                else:
                    res = Flag.CLOSE, len(data)
                break
        self.s.close()
        return res

    def print_packet(self, flag, len_data, time):
        if flag == Flag.NO_ANSWER:
            self.output = [f'{self.dest_ip}:{self.dest_port}', f'{flag.name}',
                           f'-',
                           f'-/-/- ms']
        else:
            self.output = [f'{self.dest_ip}:{self.dest_port}', f'{flag.name}',
                           f'{time} ms',
                           f'{self.min_time}/{self.avg_time}/{self.max_time} ms']

    def print_stat(self):
        percent_lose = round((self.count - self.accept_count) / self.count *
                             100, 2)
        self.avg_time = round(self.total_time / self.count, 2)
        self.output.append(f'--- {self.dest_ip} tcping statistics ---\n'
                           f'{self.count} transmitted, {self.accept_count} received '
                           f'{percent_lose}% packet loss, '
                           f'time {round(self.total_time, 2)} ms\n'
                           f'rtt min/avg/max = {self.min_time}/{self.avg_time}/'
                           f'{self.max_time} ms')
