import socket
import struct



def fake_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(('127.0.0.1', 5555))

    while True:
        data, addr = server_sock.recvfrom(1024)
        print "recieved message"
        if data:
            print len(data)
            server_sock.close()
            return data


def unpack_struct(data):
    test_str = "!cbB?hhHiIlLqQfd5s"
    return struct.unpack(test_str, data)


test_vals = ("a", 1, 2, 1, -1, 3, 2, 50, 1, 11, \
            3, 1000, 44, 3.14, 3.14, "hello")

ret = fake_server()
unpacked = unpack_struct(ret)
print unpacked
if ret == unpacked :
    print "test passed"
else:
    print "test fail"

