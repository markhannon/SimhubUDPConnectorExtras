'''Helper Class to send data via UDP stream.'''

import json
import socket

class UDPDataStream:
    '''Wrapper for UDP data stream'''
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def close(self):
        self.sock.close()
        
    def send(self, data):
        '''Send data to UDPDataStream after JSON encoding'''
        self.sock.sendto(bytes(json.dumps(data), "UTF-8"), (self.ip, self.port))
