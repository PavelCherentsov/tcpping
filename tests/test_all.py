import os
import unittest
import sys
from struct import pack
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from modules.Packet import Packet
from modules.TCPing import TCPing
from tests.server import start_server


class PacketTest(unittest.TestCase):

    def test_packet_get_ip_header(self):
        p = Packet('10.0.0.1', 1234)
        iph = p.get_ip_header(0x0)
        self.assertEqual(iph[0:12], b'E\x00\x00(\xab\xcd\x00\x00@\x06\x00\x00')
        self.assertEqual(iph[12:16], p.src_addr)
        self.assertEqual(iph[16:20], p.dest_addr)

    def test_packet_get_tcp_header(self):
        p = Packet('10.0.0.1', 1234)
        tcph = p.get_tcp_header(0x0)
        self.assertEqual(tcph[0:2], pack('!H', p.src_port))
        self.assertEqual(tcph[2:4], pack('!H', p.dest_port))
        self.assertEqual(tcph[4:20], b'\x00\x00\x00\x00\x00\x00\x00\x00P\x02q'
                                     b'\x10\x00\x00\x00\x00')

    def test_generate_packet(self):
        p = Packet('10.0.0.1', 1234)
        packet = p.generate_packet()
        self.assertEqual(packet[0:10], b'E\x00\x00(\xab\xcd\x00\x00@\x06')
        self.assertEqual(packet[12:16], p.src_addr)
        self.assertEqual(packet[16:20], p.dest_addr)
        self.assertEqual(packet[20:22], pack('!H', p.src_port))
        self.assertEqual(packet[22:24], pack('!H', p.dest_port))
        self.assertEqual(packet[24:36], b'\x00\x00\x00\x00\x00\x00\x00\x00P'
                                        b'\x02q\x10')


class TCPingTest(unittest.TestCase):
    def test_open(self):
        thread = Thread(target=start_server, daemon=True)
        thread.start()
        t = TCPing('localhost', 10000, 1, 10, 0.1)
        thread1 = Thread(target=t.ping, daemon=True)
        thread1.start()
        thread1.join(timeout=1)
        self.assertEqual(t.output[1], "OPEN")
        thread.join(timeout=1)

    def test_close(self):
        t = TCPing('localhost', 10000, 1, 10, 0.1)
        thread1 = Thread(target=t.ping, daemon=True)
        thread1.start()
        thread1.join(timeout=1)
        self.assertEqual(t.output[1], "CLOSE")

    def test_no_answer(self):
        t = TCPing('255.255.255.255', 1111, 10, 0.5, 0.5)
        thread1 = Thread(target=t.start, daemon=True)
        thread1.start()
        thread1.join(timeout=2)
        self.assertEqual(t.output[1], "-")


if __name__ == '__main__':
    unittest.main()
