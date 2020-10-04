#!/prod/moguterm/pyenv/bin/python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{prog} - serial terminal program, with command timing and readline support

Usage:
  {prog} <port> [--baud=<baud>]

Options:
  --baud=<baud>  baud rate on the serial line [default: 57600]
"""
import sys
import os
import threading
import serial
import readline
import termios
import time
from docopt import docopt
from pprint import pprint
from os.path import expanduser


def set_terminal_echo(enabled):
    fd = sys.stdin.fileno()
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(fd)

    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)


class Terminal(object):
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)
        self.run = True
        self.t = time.time()
        self.nl_state = True

    def tx(self):
        while self.run:
            try:
                line = input()
            except EOFError:
                self.run = False
                self.ser.cancel_read()
                break
            self.ser.write(line.encode("utf8") + b"\r\n")
            self.t = time.time()
            self.nl_state = True

    def rx(self):
        while self.run:
            data = self.ser.read(1)
            if data == b'':
                break
            if self.nl_state:
                sys.stdout.buffer.write(b"[%f] " % (time.time() - self.t))
                self.nl_state = False
            if data == b"\n":
                self.nl_state = True
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()

    def start(self):
        tx_t = threading.Thread(target=self.tx)
        rx_t = threading.Thread(target=self.rx)
        tx_t.daemon = True
        rx_t.daemon = True
        tx_t.start()
        rx_t.start()
        tx_t.join()
        rx_t.join()


prog = os.path.basename(sys.argv[0])
arguments = docopt(__doc__.format(prog=prog))

history_file = "%s/.%s_history" % (expanduser("~"),prog)
readline.set_history_length(3)
try:
    readline.read_history_file(history_file)
except FileNotFoundError:
    pass

print("Type some commands, terminate with either CTRL-C or eof (CTRL-D)")
try:
    Terminal(arguments['<port>'], arguments['--baud']).start()
except KeyboardInterrupt:
    pass
print("Bye")
set_terminal_echo(True)

readline.write_history_file(history_file)
