import threading
import os
import struct
import array
import time
import socket
import threading


class SendPingThread(threading.Thread):
    def __init__(self, ipPool, icmpPacket, icmpSocket, timeout=3):
        threading.Thread.__init__(self)
        self.sock = icmpSocket
        self.ipPool = ipPool
        self.packet = icmpPacket
        self.timeout = timeout
        self.sock.settimeout(timeout + 1)
    def run(self):
        time.sleep(0.01)
        for ip in self.ipPool:
            try:
                self.sock.sendto(self.packet, (ip, 0))
                # 利用套截字发送icmp包
            except socket.timeout:
                break
        time.sleep(self.timeout)


class AliveScan:
    def __init__(self, timeout=3):
        self.timeout = timeout
        self._data = struct.pack('d', time.time())
        self._id = os.getpid()

    @property
    def icmp_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        return sock

    def check_sum(self, packet):
        if len(packet) & 1:
            packet = packet + '\0'
        words = array.array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        return (~sum) & 0xffff
        # 构造校验和

    @property
    def icmp_packet(self):
        header = struct.pack('bbHHh', 8, 0, 0, self._id, 0)
        packet = header + self._data
        chkSum = self.check_sum(packet)
        header = struct.pack('bbHHh', 8, 0, chkSum, self._id, 0)
        return header + self._data

    # 构造icmp包
    def hot_ping(self, ipPool):
        sock = self.icmp_socket
        sock.settimeout(self.timeout)
        packet = self.icmp_packet
        recvFroms = set()
        sendThr = SendPingThread(ipPool, packet, sock, self.timeout)
        sendThr.start()
        while True:

            try:
                alive_ip = sock.recvfrom(1024)[1][0]
                # 接收返回值

                if alive_ip not in recvFroms:
                    #print('alive %s' % alive_ip)
                    recvFroms.add(alive_ip)
            except Exception:

                pass
            finally:
                if not sendThr.isAlive():
                    break
        print
        "recvFroms: ", recvFroms
        return recvFroms & ipPool
#ip列表判断存活


