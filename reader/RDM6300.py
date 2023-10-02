#!/usr/bin/env python
# -*- coding: utf-8 -*-

from serial import Serial, EIGHTBITS
from itertools import chain

import time

from common.constants import PERIOD_READER_MANAGER

RFID_STARTCODE  = 0x02
RFID_ENDCODE    = 0x03
SERIAL_PORT     = '/dev/ttyS0'
BAUDRATE        = 9600

serial_port = Serial(
    port        = SERIAL_PORT,
    baudrate    = BAUDRATE,
    bytesize    = EIGHTBITS,
    timeout     = 0.1
    )

def is_checksum_OK(sequence):
    checksum_calculated = 0
    for i in range(0, 10, 2):
        byte = int(sequence[i],16) << 4
        byte = byte | int(sequence[i + 1],16)
        checksum_calculated = checksum_calculated ^ byte
    
    checksum_received = int("0x"+sequence[10:12],16)

    return (checksum_received == checksum_calculated)
    
def calculate_card_id_from_sequence(sequence):
    """ sequence is made of 12 hexadecimal values from [0] to [11]
    [0]  and [1]   : type of card 
    [2]  to  [9]   : ID (printed on the card)
    [10] and [11]  : checksum 

    returns
    - card ID as an integer
    - or False
    """
    if not sequence: return False

    if len(sequence) != 12: return False

    if not is_checksum_OK(sequence): return False

    return int("0x"+sequence[2:10],16) # returns card ID 

def get_next_byte_as_integer():
    b = None
    while not b: # Blocking 
        b = serial_port.read(size=1)
    return b[0]

def wait_for_startcode():
    next_byte_as_int = 0 
    while next_byte_as_int != RFID_STARTCODE:
        next_byte_as_int = get_next_byte_as_integer() # Blocking

def get_sequence():
    sequence = ""
    next_b = 0
    while next_b != RFID_ENDCODE or len(sequence) <12:
        next_b = get_next_byte_as_integer() # Blocking
        if next_b in chain(range(48,58),range(65,71)): # ascii 0 to 9 (numbers) and A to F (hex letters)
            sequence = sequence + chr(next_b)
    return sequence

def wait_for_card():
    wait_for_startcode()
    return calculate_card_id_from_sequence(get_sequence())

def scan_card():
    # print("Waiting for 125kHz RFID card")
    serial_port.reset_input_buffer()
    card = False
    while not card:
        time.sleep(0.8)
        card = wait_for_card() # Blocking

    card_str = str(card).zfill(10)
    # print(f"card read:{card_str}")
    return card_str

#scan_card()