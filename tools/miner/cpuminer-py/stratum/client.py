import ssl
import json
import time
import socket
import logging
import random
import Queue
import threading

RECV_SIZE = 2 ** 16
CLIENT_VERSION = "0.0"
PROTO_VERSION = "1.0"

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 6002

TIMEOUT = 5

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("stratum-client")


def encode_msg(msg):
    return json.dumps(msg).encode() + b"\n"


def socket_reader(sock, queue):
    f = sock.makefile()

    while True:
        try:
            line = f.readline()
        except socket.timeout:
            continue
        except (socket.error, ssl.SSLError) as e:
            log.error("error reading from socket: %s", e)
            break
        if not line:
            break
        # log.debug(">>> %s", line.strip())
        msg = json.loads(line.strip())
        queue.put(msg)
    sock.close()


def socket_writer(sock, queue):
    while True:
        msg = queue.get()
        if not msg:
            break
        try:
            payload = encode_msg(msg)
            # log.debug("<<< %s", payload.strip())
            sock.send(payload)
        except (socket.error, ssl.SSLError) as e:
            log.error("error writing from socket: %s", e)
            break
    sock.close()


class Connection(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, ssl=False):
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.ssl = ssl
        self.call_count = 0

        self.socket = None
        self.server_version = None

        self.reader = None
        self.writer = None
        self.incoming = Queue.Queue()
        self.outgoing = Queue.Queue()

        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_socket(self):
        sock = socket.create_connection((self.host, self.port), timeout=TIMEOUT)
        return ssl.wrap_socket(sock) if self.ssl else sock

    def connect(self):
        log.debug("connecting to %s:%s...", self.host, self.port)
        self.socket = self.create_socket()
        log.info("connected to %s:%s", self.host, self.port)

        self.reader = threading.Thread(target=socket_reader, args=(self.socket, self.incoming))
        self.reader.setDaemon(True)
        self.reader.start()

        self.writer = threading.Thread(target=socket_writer, args=(self.socket, self.outgoing))
        self.writer.setDaemon(True)
        self.writer.start()

        #self.version()

    def version(self):
        self.server_version = self.call("server.version")["result"]

    def close(self):
        self.socket.close()
        log.info("disconnected from %s:%s", self.host, self.port)
        self.socket = None

    def send(self, method, params):
        msg = {"id": self.call_count, "method": method, "params": params}
        self.call_count += 1
        self.outgoing.put(msg)

    def recv(self):
        return self.incoming.get()

    def call(self, method, *params):
        t1 = time.time()
        self.send(method, params)
        resp = self.recv()
        t2 = time.time()
        delta = (t2 - t1) * 1000
        log.debug("%s(%s) took %sms", method, params, delta)
        return resp


class Peer(object):

    ADDRESS_TYPE_CLEAR = "c"
    ADDRESS_TYPE_ONION = "o"
    ADDRESS_TYPE_ANY = "a"

    PORT_TYPE_TCP = "t"
    PORT_TYPE_SSL = "s"
    PORT_TYPE_HTTP = "h"
    PORT_TYPE_HTTPS = "g"
    PORT_TYPES = (PORT_TYPE_TCP, PORT_TYPE_SSL, PORT_TYPE_HTTP, PORT_TYPE_HTTPS)

    def __init__(self, addresses, params):
        self.addresses = addresses
        self.params = params
        self.verison = params[0]
        self.prune = None
        self.ports = []
        self.parse(params)

    def parse(self, params):
        for param in params:
            if param[0] == "p":
                self.prune = int(param[1:])
            elif param[0] in self.PORT_TYPES:
                peer_type = param[0]
                if param[1:]:
                    port = int(param[1:])
                elif peer_type == self.PORT_TYPE_TCP:
                    port = DEFAULT_PORT
                elif peer_type == self.PORT_TYPE_SSL:
                    port = 50002
                elif peer_type == self.PORT_TYPE_HTTP:
                    port = 8081
                elif peer_type == self.PORT_TYPE_HTTPS:
                    port = 8082

                if port:
                    self.ports.append((peer_type, port))

    def __repr__(self):
        return "Peer(addresses={}, params={})".format(self.addresses, self.params)

    @classmethod
    def discover(cls):
        with Connection() as conn:
            result = conn.call("server.peers.subscribe")
        peers = result["result"]
        return [Peer(peer[0:-1], peer[-1]) for peer in peers]

    @property
    def all_addresses(self):
        return [address for address in self.addresses]

    @property
    def clearnet_addresses(self):
        return [address for address in self.addresses if not is_onion(address)]

    @property
    def onion_addresses(self):
        return [address for address in self.addresses if is_onion(address)]

    def get_ports_by_type(self, port_type):
        return [port for pt, port in self.ports if port_type == pt]

    tcp_ports = property(lambda self: self.get_ports_by_type(self.PORT_TYPE_TCP))
    ssl_ports = property(lambda self: self.get_ports_by_type(self.PORT_TYPE_SSL))
    http_ports = property(lambda self: self.get_ports_by_type(self.PORT_TYPE_HTTP))
    https_ports = property(lambda self: self.get_ports_by_type(self.PORT_TYPE_HTTPS))


def is_onion(address):
    return address.endswith(".onion")


class ConnectionHandler(object):
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.connection = None

    def __enter__(self):
        self.connection = self.connection_pool.take()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection_pool.release(self.connection)


def connect_to_peer(peers, allow_tcp=True, address_type=Peer.ADDRESS_TYPE_CLEAR):
    for _ in range(100):

        peer = random.choice(peers)

        if address_type == Peer.ADDRESS_TYPE_CLEAR:
            addresses = peer.clearnet_addresses
        elif address_type == Peer.ADDRESS_TYPE_ONION:
            addresses = peer.onion_addresses
        else:
            addresses = peer.all_addresses

        if not addresses:
            continue

        ports = peer.ssl_ports
        has_ssl = bool(ports)
        if not has_ssl and allow_tcp:
            ports = peer.tcp_ports

        if not ports:
            continue

        address = addresses[0]
        port = ports[0]
        try:
            return Connection(host=address, port=port, ssl=has_ssl)
        except socket.error as e:
            log.error("could not connect to %s: %s", address, e)


class ConnectionPool(object):
    def __init__(self, max_size):
        self.connections = Queue.Queue()
        self.peers = Peer.discover()
        self.max_size = max_size
        self.count = 0

    def get(self):
        return ConnectionHandler(self)

    def close(self):
        while not self.connections.empty():
            connection = self.connections.get_nowait()
            connection.close()

    def release(self, connection):
        self.connections.put(connection)

    def new_connection(self):
        conn = connect_to_peer(self.peers)
        if conn:
            self.count += 1
        return conn

    def take(self):
        block = self.count >= self.max_size
        try:
            connection = self.connections.get(block=block)
        except Queue.Empty:
            connection = self.new_connection()
        return connection

if __name__ == "__main__":
    conn = Connection(1)
    result = conn.call("mining.subscribe")["result"]
    print("result ", result)

