import socket
from .Packet import Packet
from time import sleep
from timeit import default_timer
from math import inf


class TCPing:
    def __init__(self, output, dest_ip, dest_port, count, timeout, interval):
        self.s = None
        self.output = output
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.count = count
        self.accept_count = 0
        self.timeout = timeout
        self.interval = interval

        self.total_time = 0
        self.min_time = inf
        self.max_time = 0

        p = Packet(socket.gethostbyname(dest_ip), self.dest_port)
        self.packet = p.generate_packet()

        self.output(f'TCPing {dest_ip} ({p.dest_ip}:{p.dest_port}).')

        for i in range(count):
            s_start = default_timer()

            self.send_packet(self.packet)
            syn_ack, len_data = self.recv_packet()

            s_stop = default_timer()

            time = round(1000 * (s_stop - s_start), 2)

            self.total_time += time
            self.min_time = min(self.min_time, time)
            self.max_time = max(self.max_time, time)

            self.print_packet(syn_ack, len_data, time)

            sleep(interval)

        self.print_stat()

    def send_packet(self, packet):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                               socket.IPPROTO_TCP)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.s.sendto(packet, (self.dest_ip, 0))

    def recv_packet(self):
        self.s.settimeout(self.timeout)
        while True:
            try:
                data = self.s.recv(1024)
            except socket.timeout:
                res = False, 0
                break
            if data[20:22] == self.packet[22:24] \
                    and data[22:24] == self.packet[20:22]:
                if data[33:34] == b'\x12':
                    self.accept_count += 1
                    res = True, len(data)
                else:
                    res = False, len(data)
                break
        self.s.close()
        return res

    def print_packet(self, syn_ack, len_data, time):
        if len_data == 0:
            self.output(f'NO ANSWER \t from {self.dest_ip}:{self.dest_port}')
        elif syn_ack:
            self.output(f'SYN ACK \t {len_data} bytes from '
                        f'{self.dest_ip}:{self.dest_port} \t time={time} ms')
        else:
            self.output(f'RST \t {len_data} bytes from '
                        f'{self.dest_ip}:{self.dest_port} \t time={time} ms')

    def print_stat(self):
        percent_lose = round((self.count - self.accept_count) / self.count *
                             100, 2)
        avg_time = round(self.total_time / self.count, 2)
        self.output(f'--- {self.dest_ip} tcping statistics ---\n'
                    f'{self.count} transmitted, {self.accept_count} received '
                    f'{percent_lose}% packet loss, '
                    f'time {round(self.total_time, 2)} ms\n'
                    f'rtt min/avg/max = {self.min_time}/{avg_time}/'
                    f'{self.max_time} ms')
