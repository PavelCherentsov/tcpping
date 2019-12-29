import socket
from struct import pack


def get_ip_port_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()


class Packet:
    VERSION = 0x4
    IHL = 0x5
    TYPE_OF_SERVICE = 0x0
    TOTAL_LENGTH = 0x28
    IDENTIFICATION = 0xabcd
    FLAGS = 0x0
    FRAGMENT_OFFSET = 0x0
    TTL = 0x40
    PROTOCOL = 0x6
    HEADER_CHECKSUM = 0x0

    V_IHL = (VERSION << 4) + IHL
    F_FO = (FLAGS << 13) + FRAGMENT_OFFSET

    IP_HEADER_TO_CHECKSUM = pack("!BBHHHBB",
                                 V_IHL,
                                 TYPE_OF_SERVICE,
                                 TOTAL_LENGTH,
                                 IDENTIFICATION,
                                 F_FO,
                                 TTL,
                                 PROTOCOL)

    SEQ_NO = 0x0
    ACK_NO = 0x0
    DATA_OFFSET = 0x5
    RESERVED = 0x0
    TCP_SYN = 0x2
    WINDOW_SIZE = 0x7110
    URG_POINTER = 0x0

    DATA_OFFSET_RES_FLAGS = ((DATA_OFFSET << 12) +
                             (RESERVED << 9) + TCP_SYN)

    TCP_HEADER_BETWEEN_PORTS_CHECKSUM = pack("!LLHH",
                                             SEQ_NO,
                                             ACK_NO,
                                             DATA_OFFSET_RES_FLAGS,
                                             WINDOW_SIZE)

    def __init__(self, dest_ip, dest_port):
        my_ip, my_port = get_ip_port_address()

        self.src_ip = my_ip
        self.dest_ip = dest_ip
        self.src_addr = socket.inet_aton(self.src_ip)
        self.dest_addr = socket.inet_aton(self.dest_ip)

        self.src_port = my_port
        self.dest_port = dest_port

        self.tcp_header = b""
        self.ip_header = b""
        self.packet = self.ip_header + self.tcp_header

    @staticmethod
    def get_checksum(msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + msg[i + 1]
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

    def get_ip_header(self, checksum):
        return Packet.IP_HEADER_TO_CHECKSUM + pack("!H4s4s",
                                                   checksum,
                                                   self.src_addr,
                                                   self.dest_addr)

    def get_tcp_header(self, checksum):
        return (pack("!HH", self.src_port, self.dest_port) +
                Packet.TCP_HEADER_BETWEEN_PORTS_CHECKSUM +
                pack("!HH", checksum, Packet.URG_POINTER))

    def generate_packet(self):
        temp_ip_header = self.get_ip_header(0x0)
        temp_tcp_header = self.get_tcp_header(0x0)
        pseudo_header = pack("!4s4sBBH",
                             self.src_addr,
                             self.dest_addr,
                             0x0,
                             Packet.PROTOCOL,
                             len(temp_tcp_header))
        psh = pseudo_header + temp_tcp_header

        self.ip_header = self.get_ip_header(self.get_checksum(temp_ip_header))
        self.tcp_header = self.get_tcp_header(self.get_checksum(psh))

        self.packet = self.ip_header + self.tcp_header
        return self.packet

    TCP_SYN_ACK = b'\x12'

    @staticmethod
    def get_scr_ip(data):
        return data[20:22]

    @staticmethod
    def get_dept_ip(data):
        return data[22:24]

    @staticmethod
    def get_flag(data):
        return data[33:34]
