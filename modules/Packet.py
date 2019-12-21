import socket
from struct import pack


def get_ip_port_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()


class Packet:
    version = 0x4
    ihl = 0x5
    type_of_service = 0x0
    total_length = 0x28
    identification = 0xabcd
    flags = 0x0
    fragment_offset = 0x0
    ttl = 0x40
    protocol = 0x6
    header_checksum = 0x0

    v_ihl = (version << 4) + ihl
    f_fo = (flags << 13) + fragment_offset

    ip_header_to_checksum = pack("!BBHHHBB",
                                 v_ihl,
                                 type_of_service,
                                 total_length,
                                 identification,
                                 f_fo,
                                 ttl,
                                 protocol)

    seq_no = 0x0
    ack_no = 0x0
    data_offset = 0x5
    reserved = 0x0
    tcp_flags_syn = 0x2
    window_size = 0x7110
    urg_pointer = 0x0

    data_offset_res_flags = (data_offset << 12) + \
                            (reserved << 9) + tcp_flags_syn

    tcp_header_between_ports_checksum = pack("!LLHH",
                                             seq_no,
                                             ack_no,
                                             data_offset_res_flags,
                                             window_size)

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
        return Packet.ip_header_to_checksum + pack("!H4s4s",
                                                   checksum,
                                                   self.src_addr,
                                                   self.dest_addr)

    def get_tcp_header(self, checksum):
        return pack("!HH", self.src_port, self.dest_port) + \
               Packet.tcp_header_between_ports_checksum + \
               pack("!HH", checksum, Packet.urg_pointer)

    def generate_packet(self):
        temp_ip_header = self.get_ip_header(0x0)
        temp_tcp_header = self.get_tcp_header(0x0)
        pseudo_header = pack("!4s4sBBH",
                             self.src_addr,
                             self.dest_addr,
                             0x0,
                             Packet.protocol,
                             len(temp_tcp_header))
        psh = pseudo_header + temp_tcp_header

        self.ip_header = self.get_ip_header(self.get_checksum(temp_ip_header))
        self.tcp_header = self.get_tcp_header(self.get_checksum(psh))

        self.packet = self.ip_header + self.tcp_header
        return self.packet
