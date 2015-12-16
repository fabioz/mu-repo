# Fork: https://github.com/fabioz/u-msgpack-python
#
'''
This module provides a way to do full-duplex communication over a socket with umsgpack_s.


Basic usage is:

    # Create our server handler (must handle decoded messages)

    class ServerHandler(ConnectionHandler, UMsgPacker):

        def _handle_decoded(self, decoded):
            # Some message was received from the client in the server.
            if decoded == 'echo':
                # Actual implementations may want to put that in a queue and have an additional
                # thread to check the queue and handle what was received and send the results back.
                self.send('echo back')

        def send(self, obj):
            # Send a message to the client
            self.connection.sendall(self.pack_obj(obj))


    # Start the server
    server = umsgpack_s_conn.Server(ServerHandler)
    server.serve_forever('127.0.0.1', 0, block=True)
    port = server.get_port() # Port only available after socket is created

    ...

    On the client side:

    class ClientHandler(ConnectionHandler, UMsgPacker):

        def _handle_decoded(self, decoded):
            print('Client received: %s' % (decoded,))

    client = umsgpack_s_conn.Client('127.0.0.1', port, ClientHandler)

    # Note, as above, actual implementations may want to put that in a queue and have an additional
    # thread do the actual send.
    client.send('echo')

@license: MIT
@author: Fabio Zadrozny
'''

from mu_repo import umsgpack_s
import binascii
import select
import socket
import struct
import sys
import threading
import weakref

try:
    basestring
except:
    basestring = str

_as_bytes = umsgpack_s._as_bytes
DEBUG = 0  # > 3 to see actual messages
BUFFER_SIZE = 1024 * 8
MAX_INT32 = 2147483647  # ((2** 32) -1)


def get_free_port():
    '''
    Helper to get free port (usually not needed as the server can receive '0' to connect to a new
    port).
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    _, port = s.getsockname()
    s.close()
    return port


def wait_for_condition(condition, timeout=2.):
    '''
    Helper to wait for a condition with a timeout.
    :param float condition:
        Timeout to reach condition (in seconds).

    :return bool:
        True if the condition wasn't satisfied and True if it was.
    '''
    import time
    initial = time.time()
    while not condition():
        if time.time() - initial > timeout:
            return False
        time.sleep(.01)
    return True


def assert_waited_condition(condition, timeout=2.):
    '''
    Helper to wait for a condition with a timeout.

    :param callable condition:
        A callable that returns either a True/False boolean (where True indicates the condition was
        reached) or a string (where an empty string means the condition was reached or a non-empty
        string to show some message to the user regarding the failure).

    :param float condition:
        Timeout to reach condition (in seconds).
    '''
    import time
    initial = time.time()
    while True:
        c = condition()
        if isinstance(c, bool):
            if c:
                return
        elif isinstance(c, basestring):
            if not c:
                return
        else:
            raise AssertionError('Expecting bool or string as the return.')

        if time.time() - initial > timeout:
            raise AssertionError(
                u'Could not reach condition before timeout: %s (condition return: %s)' %
                (timeout, c))
        time.sleep(.01)


class Server(object):

    def __init__(self, connection_handler_class=None, params=(), thread_name='', thread_class=None):
        if thread_class is None:
            thread_class = threading.Thread
        self._thread_class = thread_class
        if connection_handler_class is None:
            connection_handler_class = EchoHandler
        self.connection_handler_class = connection_handler_class
        self._params = params
        self._block = None
        self._shutdown_event = threading.Event()
        self._thread_name = thread_name

    def serve_forever(self, host, port, block=False):
        if self._block is not None:
            raise AssertionError(
                'Server already started. Please create new one instead of trying to reuse.')
        if not block:
            self.thread = self._thread_class(target=self._serve_forever, args=(host, port))
            self.thread.setDaemon(True)
            if self._thread_name:
                self.thread.setName(self._thread_name)
            self.thread.start()
        else:
            self._serve_forever(host, port)
        self._block = block

    def is_alive(self):
        if self._block is None:
            return False

        sock = getattr(self, '_sock', None)
        return sock is not None

    def get_port(self):
        '''
        Note: only available after socket is already connected. Raises AssertionError if it's not
        connected at this point.
        '''
        wait_for_condition(lambda: hasattr(self, '_sock'), timeout=5.0)
        return self._sock.getsockname()[1]

    def shutdown(self):
        if DEBUG:
            sys.stderr.write('Shutting down server.\n')

        self._shutdown_event.set()
        sock = getattr(self, '_sock', None)
        if sock is not None:
            self._sock = None
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                sock.close()
            except:
                pass

    def after_bind_socket(self, host, port):
        '''
        Clients may override to do something after the host/port is bound.
        '''

    def _serve_forever(self, host, port):
        if DEBUG:
            sys.stderr.write('Listening at: %s (%s)\n' % (host, port))

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # We should cleanly call shutdown, but just in case let's set to reuse the address.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((host, port))
        sock.listen(5)  # Request queue size

        self._sock = sock
        self.after_bind_socket(host, self.get_port())
        connections = []

        try:
            while not self._shutdown_event.is_set():

                sock = self._sock
                if sock is None:
                    break

                # Will block until available (no timeout). If closed returns properly.
                try:
                    fd_sets = select.select([sock], [], [])
                except:
                    break  # error: (9, 'Bad file descriptor')
                if DEBUG:
                    sys.stderr.write('Select returned: %s\n' % fd_sets[0])

                if self._shutdown_event.is_set():
                    break

                sock = self._sock
                if sock is None:
                    break

                if fd_sets[0]:
                    connection, _client_address = sock.accept()
                    if DEBUG:
                        sys.stderr.write('Accepted socket.\n')

                    try:
                        connection_handler = self.connection_handler_class(
                            connection,
                            *self._params)
                        connections.append(weakref.ref(connection))
                        connection_handler.start()
                    except:
                        import traceback
                        traceback.print_exc()
        finally:
            if DEBUG:
                sys.stderr.write('Exited _serve_forever.\n')

            for c in connections:
                c = c()
                if c is not None:
                    try:
                        c.shutdown(socket.SHUT_RDWR)
                    except:
                        pass
                    try:
                        c.close()
                    except:
                        pass

            self.shutdown()


class UMsgPacker(object):

    '''
    Helper to pack some object as bytes to the socket.
    '''

    def pack_obj(self, obj):
        '''
        Mostly packs the object with umsgpack_s then adds the size (in bytes) to the front of the msg
        and returns it to be passed on the socket..

        :param object obj:
            The object to be packed.
        '''
        msg = umsgpack_s.packb(obj)
        assert msg.__len__() < MAX_INT32, 'Message from object received is too big: %s bytes' % (
            msg.__len__(),)
        msg_len_in_bytes = struct.pack("<I", msg.__len__())
        return(msg_len_in_bytes + msg)


class Client(UMsgPacker):

    def __init__(self, host, port, connection_handler_class=None):
        '''
        :param connection_handler_class: if passed, this is a full-duplex communication (so, handle
            incoming requests from server).
        '''
        if DEBUG:
            sys.stderr.write('Connecting to server at: %s (%s)\n' % (host, port))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))

        if connection_handler_class:
            connection_handler = self.connection_handler = connection_handler_class(self._sock)
            connection_handler.start()
            
    def get_host_port(self):
        try:
            return self._sock.getsockname()
        except:
            return None, None
        
    def is_alive(self):
        try:
            self._sock.getsockname()
            return True
        except:
            return False

    def send(self, obj):
        s = self._sock
        if s is None:
            raise RuntimeError('Connection already closed')
        self._sock.sendall(self.pack_obj(obj))
        
    def shutdown(self):
        s = self._sock
        if self._sock is None:
            return
        self._sock = None
        try:
            s.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            s.close()
        except:
            pass

class ConnectionHandler(threading.Thread, UMsgPacker):

    def __init__(self, connection, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        self.connection = connection
        try:
            connection.settimeout(None)  # No timeout
        except:
            pass

    def run(self):
        data = _as_bytes('')
        number_of_bytes = 0
        try:
            while True:
                # I.e.: check if the remaining bytes from our last recv already contained
                # a new message.
                if number_of_bytes == 0 and data.__len__() >= 4:
                    number_of_bytes = data[
                        :4]  # first 4 bytes say the number_of_bytes of the message
                    number_of_bytes = struct.unpack("<I", number_of_bytes)[0]
                    assert number_of_bytes >= 0, 'Error: wrong message received. Shutting down connection!'
                    data = data[4:]  # The remaining is the actual data

                while not data or number_of_bytes == 0 or data.__len__() < number_of_bytes:

                    if DEBUG > 3:
                        sys.stderr.write('%s waiting to receive.\n' % (self,))

                    try:
                        # It's usually waiting here: when the remote side disconnects, that's
                        # where we get an exception.
                        rec = self.connection.recv(BUFFER_SIZE)
                        if len(rec) == 0:
                            if DEBUG:
                                sys.stderr.write('Disconnected (socket closed).\n')
                            return
                    except:
                        if DEBUG:
                            sys.stderr.write('Disconnected.\n')
                        return

                    if DEBUG > 3:
                        sys.stderr.write('%s received: %s\n' % (self, binascii.b2a_hex(rec)))

                    data += rec
                    if not number_of_bytes and data.__len__() >= 4:
                        number_of_bytes = data[
                            :4]  # first 4 bytes say the number_of_bytes of the message
                        number_of_bytes = struct.unpack("<I", number_of_bytes)[0]
                        assert number_of_bytes >= 0, 'Error: wrong message received. Shutting down connection!'
                        data = data[4:]  # The remaining is the actual data
                        if DEBUG:
                            sys.stderr.write('Number of bytes expected: %s\n' % number_of_bytes)
                            sys.stderr.write('Current data len: %s\n' % data.__len__())

                msg = data[:number_of_bytes]
                data = data[number_of_bytes:]  # Keep the remaining for the next message
                number_of_bytes = 0
                self._handle_msg(msg)

        finally:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.connection.close()
            except:
                pass

    def _handle_msg(self, msg_as_bytes):
        if DEBUG > 3:
            sys.stderr.write('%s handling message: %s\n' % (self, binascii.b2a_hex(msg_as_bytes)))
        decoded = umsgpack_s.unpackb(msg_as_bytes)
        self._handle_decoded(decoded)

    def _handle_decoded(self, decoded):
        pass


class EchoHandler(ConnectionHandler):

    def _handle_decoded(self, decoded):
        sys.stdout.write('%s\n' % (decoded,))


if __name__ == '__main__':
    # Simple example of client-server.
    import time

    class ServerHandler(ConnectionHandler, UMsgPacker):

        def _handle_decoded(self, decoded):
            # Some message was received from the client in the server.
            if decoded == 'echo':
                # Actual implementations may want to put that in a queue and have an additional
                # thread to check the queue and handle what was received and send the results back.
                self.send('echo back')

        def send(self, obj):
            # Send a message to the client
            self.connection.sendall(self.pack_obj(obj))

    # Start the server
    server = Server(ServerHandler)
    # Note: not blocking means it'll start in another thread
    server.serve_forever('127.0.0.1', 0, block=False)

    time.sleep(2)  # Wait for the other thread to actually start the server.

    port = server.get_port()  # Port only available after socket is created

    received = [False]

    class ClientHandler(ConnectionHandler, UMsgPacker):

        def _handle_decoded(self, decoded):
            print('Client received: %s' % (decoded,))
            received[0] = True

    client = Client('127.0.0.1', port, ClientHandler)

    # Note, as above, actual implementations may want to put that in a queue and have an additional
    # thread do the actual send.
    client.send('echo')
    assert_waited_condition(lambda: received[0])
