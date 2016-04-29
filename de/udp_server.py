# -*- coding: utf-8 -*-
from errno import EWOULDBLOCK, EAGAIN
import logging
import os
import socket

from tornado.ioloop   import IOLoop
from tornado.netutil  import set_close_exec


from logging.handlers import RotatingFileHandler
from settings         import LOG_FILE_NAME
from settings         import LOG_PORT

def create_client():
    ''' '''
    udp_sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return udp_sock

udp_sock     = create_client()
def send_msg(msg):
    udp_sock.sendto(msg, ('localhost', LOG_PORT))


#----------------------------------------------------------------------
def create_logger(path):
    """ 创建logger """
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)
    logging.Formatter('%(message)s')
    handler = RotatingFileHandler(path, maxBytes=1024*1024*1024,
                                  backupCount=1000)
    logger.addHandler(handler)
 
    return logger

logger          = create_logger(LOG_FILE_NAME)
logger.propagate=0 #不打印log出来


class UDPServer(object):
    def __init__(self, name, port, on_receive, address=None, family=socket.AF_INET, io_loop=None):
        self.io_loop     = io_loop or IOLoop.instance()
        self._on_receive = on_receive
        self._sockets = []

        flags = socket.AI_PASSIVE

        if hasattr(socket, "AI_ADDRCONFIG"):
            flags |= socket.AI_ADDRCONFIG

        # find all addresses to bind, bind and register the "READ" callback
        for res in set(socket.getaddrinfo(address, port, family, socket.SOCK_DGRAM, 0, flags)):
            af, sock_type, proto, canon_name, sock_addr = res
            self._open_and_register(af, sock_type, proto, sock_addr)

        print('Started')

    def _open_and_register(self, af, sock_type, proto, sock_addr):
        sock = socket.socket(af, sock_type, proto)
        set_close_exec(sock.fileno())
        if os.name != 'nt':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)

        print('Binding to %s...', repr(sock_addr))
        sock.bind(sock_addr)

        def read_handler(fd, events):
            while True:
                try:
                    data, address = sock.recvfrom(65536)
                except socket.error as e:
                    if e.args[0] in (EWOULDBLOCK, EAGAIN):
                        return
                    raise
                self._on_receive(data, address)

        self.io_loop.add_handler(sock.fileno(), read_handler, IOLoop.READ)
        self._sockets.append(sock)

    def stop(self):
        print('Closing %d socket(s)...', len(self._sockets))
        for sock in self._sockets:
            self.io_loop.remove_handler(sock.fileno())
            sock.close()


def custom_on_receive(data, address):
    logger.info(data)


def main():
    server = UDPServer('meifenfen_api_logger_on_8008', LOG_PORT, on_receive=custom_on_receive)

#     def done(*args):
#         print args
#         for stoppable in args:
#             stoppable.stop()
#     IOLoop.instance().call_later(10, done, server, IOLoop.instance())

    IOLoop.instance().start()


if __name__ == '__main__':
    main()
