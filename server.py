import socket
import random
import atexit

class ClientConnection:
    def __init__(self, s: socket.socket) -> None:
        """
        Creates a ClientConnection.
        - `s` should be an open client socket in non-blocking mode.
        """
        atexit.register(self.disconnect) # make sure socket is closed on crash

        self.socket: socket.socket = s
        self.inboundbuffer = bytearray()      # buffer of inbound bytes
        self.outboundbuffer = bytearray()     # buffer of outbound bytes
        self.inboundmessages: list[str] = []  # queue of inbound messages
        self.outboundmessages: list[str] = [] # queue of outbound messages
    
    def process(self) -> None:
        """
        Call this in the main process (game) loop.
        Updates the state of the ClientConnection:
        - receives inbound data
        - extracts complete messages (newline-terminated ascii strings)
        - sends outbound data
        """
        inboundbytes = self._get_bytes()
        if inboundbytes != b'':
            inboundmessage = inboundbytes.decode('ascii')
            self.inboundmessages.append(inboundmessage)

        outbytes = bytearray()
        for m in self.outboundmessages:
            fullmessage = m + '\n'
            fullmessagebytes = fullmessage.encode('ascii')
            outbytes += bytearray(fullmessagebytes)
        self.outboundmessages.clear()
        self._send_bytes(bytes(outbytes))

    def get_messages(self) -> list[str]:
        """
        Gets all messages in the inbound message queue and clears the queue.
        """
        messages = self.inboundmessages.copy()
        self.inboundmessages.clear()
        return messages
    
    def send_message(self, message: str) -> None:
        """
        Adds a message to the outbound message queue.
        """
        self.outboundmessages.append(message)
        return
    
    def _get_bytes(self) -> bytes:
        """
        Returns a full message if one was received, or an empty bytes object
        otherwise.
        - Adds received bytes to the inbound byte buffer.
        - Detects complete messages by finding newline characters (ascii 0x0A).
        - Should probably only be called once per process loop.
        TODO: Allow extracting/returning more than 1 message at a time.
        """
        try:
            inbounddata: bytes = self.socket.recv(1024)
        except BlockingIOError:
            return b''
        
        self.inboundbuffer += bytearray(inbounddata)

        # find message delimiter (newline)
        #while i != -1:
        i = self.inboundbuffer.find(b'\x0A')
        if i != -1:
            message = bytes(self.inboundbuffer[:i]) # the message, excluding newline
            self.inboundbuffer = self.inboundbuffer[i+1:] # remove message from buffer, including newline
            return message
        
        return b''
    
    def _send_bytes(self, message: bytes) -> None:
        """
        Adds bytes to the outbound byte buffer and sends as many as possible.
        - Should probably only be called once per process loop.
        """
        self.outboundbuffer += bytearray(message)

        try:
            numsent = self.socket.send(self.outboundbuffer)
        except BlockingIOError:
            return
        
        self.outboundbuffer = self.outboundbuffer[numsent:] # remove sent bytes from buffer
        return
    
    def disconnect(self) -> None:
        """
        Cleans up resources:
        - Closes the socket. Note that this doesn't actually free the socket
          (see http://www.faqs.org/faqs/unix-faq/socket/ sections 2.5 and 2.7).
        """
        self.socket.close()

def accept_connection(serversocket: socket.socket) -> socket.socket:
    try:
        clientsocket, clientaddress = serversocket.accept()
        clientsocket.setblocking(False)
    except BlockingIOError:
        return None
    
    return clientsocket

def start_server(ip: str, port: int) -> socket.socket:
    """
    Initializes and returns a server socket in non-blocking mode.
    - `ip` is the server ip, can be like '192.168.0.1' or 'localhost'.
    - `port` is the server port, should probably be a high number (>1024).
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((ip, port))
    serversocket.listen()
    serversocket.setblocking(False)
    return serversocket

if __name__ == '__main__':

    # create a server socket
    serverip = 'localhost'
    serverport = 42000 + random.randint(0, 10) # random ports for easier testing
    serversocket = start_server(serverip, serverport)
    print(f'server started on port {serverport}')

    # main process loop
    clientconnections: list[ClientConnection] = []
    lastmessage = ''
    while True:

        # accept any incoming connections
        s = accept_connection()
        if not s is None:
            cc = ClientConnection(s)
            clientconnections.append(cc)
            print('new connection!')
        
        for cc in clientconnections:
            cc.process()
        
        # receive any inbound messages
        for cc in clientconnections:
            ms = cc.get_messages()
            for m in ms:
                print(m)

                if m == 'disconnect':
                    print('goodbye')
                
                if m == 'crash':
                    1 / 0
                
                if m == 'ping':
                    cc.send_message('pong')

    for cc in clientconnections:
        cc.disconnect()
    serversocket.close()
