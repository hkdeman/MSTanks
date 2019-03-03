import json
import socket
import logging
import binascii
import struct
import argparse
import random

class ServerMessageTypes(object):
    TEST = 0
    CREATETANK = 1
    DESPAWNTANK = 2
    FIRE = 3
    TOGGLEFORWARD = 4
    TOGGLEREVERSE = 5
    TOGGLELEFT = 6
    TOGGLERIGHT = 7
    TOGGLETURRETLEFT = 8
    TOGGLETURRETRIGHT = 9
    TURNTURRETTOHEADING = 10
    TURNTOHEADING = 11
    MOVEFORWARDDISTANCE = 12
    MOVEBACKWARSDISTANCE = 13
    STOPALL = 14
    STOPTURN = 15
    STOPMOVE = 16
    STOPTURRET = 17
    OBJECTUPDATE = 18
    HEALTHPICKUP = 19
    AMMOPICKUP = 20
    SNITCHPICKUP = 21
    DESTROYED = 22
    ENTEREDGOAL = 23
    KILL = 24
    SNITCHAPPEARED = 25
    GAMETIMEUPDATE = 26
    HITDETECTED = 27
    SUCCESSFULLHIT = 28

    strings = {
        TEST: "TEST",
        CREATETANK: "CREATETANK",
        DESPAWNTANK: "DESPAWNTANK",
        FIRE: "FIRE",
        TOGGLEFORWARD: "TOGGLEFORWARD",
        TOGGLEREVERSE: "TOGGLEREVERSE",
        TOGGLELEFT: "TOGGLELEFT",
        TOGGLERIGHT: "TOGGLERIGHT",
        TOGGLETURRETLEFT: "TOGGLETURRETLEFT",
        TOGGLETURRETRIGHT: "TOGGLETURRENTRIGHT",
        TURNTURRETTOHEADING: "TURNTURRETTOHEADING",
        TURNTOHEADING: "TURNTOHEADING",
        MOVEFORWARDDISTANCE: "MOVEFORWARDDISTANCE",
        MOVEBACKWARSDISTANCE: "MOVEBACKWARDSDISTANCE",
        STOPALL: "STOPALL",
        STOPTURN: "STOPTURN",
        STOPMOVE: "STOPMOVE",
        STOPTURRET: "STOPTURRET",
        OBJECTUPDATE: "OBJECTUPDATE",
        HEALTHPICKUP: "HEALTHPICKUP",
        AMMOPICKUP: "AMMOPICKUP",
        SNITCHPICKUP: "SNITCHPICKUP",
        DESTROYED: "DESTROYED",
        ENTEREDGOAL: "ENTEREDGOAL",
        KILL: "KILL",
        SNITCHAPPEARED: "SNITCHAPPEARED",
        GAMETIMEUPDATE: "GAMETIMEUPDATE",
        HITDETECTED: "HITDETECTED",
        SUCCESSFULLHIT: "SUCCESSFULLHIT"
    }

    def toString(self, id):
        if id in self.strings.keys():
            return self.strings[id]
        else:
            return "??UNKNOWN??"

class ServerComms(object):
    '''
    TCP comms handler
    Server protocol is simple:
    * 1st byte is the message type - see ServerMessageTypes
    * 2nd byte is the length in bytes of the payload (so max 255 byte payload)
    * 3rd byte onwards is the payload encoded in JSON
    '''
    server_socket = None
    message_types = ServerMessageTypes()
    
    def __init__(self, hostname, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.connect((hostname, port))

    def read_message(self):
        '''
        Read a message from the server
        '''
        message_typeRaw = self.server_socket.recv(1)
        messageLenRaw = self.server_socket.recv(1)
        message_type = struct.unpack('>B', message_typeRaw)[0]
        messageLen = struct.unpack('>B', messageLenRaw)[0]

        if messageLen == 0:
            messageData = bytearray()
            message_payload = None
        else:
            messageData = self.server_socket.recv(messageLen)
            logging.debug("*** {}".format(messageData))
            try:
                message_payload = json.loads(messageData.decode('utf-8'))
            except:
                return None
        
        logging.debug('Turned message {} into type {} payload {}'.format(
            binascii.hexlify(messageData),
            self.message_types.toString(message_type),
            message_payload))
        return dict(type=message_type, data=message_payload)

    def send_message(self, message_type=None, message_payload=None):
        '''
        Send a message to the server
        '''
        message = bytearray()
        if message_type is not None:
            message.append(message_type)
        else:
            message.append(0)

        if message_payload is not None:
            message_string = json.dumps(message_payload)
            message.append(len(message_string))
            message.extend(str.encode(message_string))
        else:
            message.append(0)

        logging.debug('Turned message type {} payload {} into {}'.format(
            self.message_types.toString(message_type),
            message_payload,
            binascii.hexlify(message)))
        return self.server_socket.send(message)