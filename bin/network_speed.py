# copy from stackoverflow


import threading
import time
from collections import deque
import psutil
from argparse import ArgumentParser
import platform
import os
import sys 

time_interval = 0.5


def calc_ul_dl(rate, dt=time_interval, interface="en0"):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True).get(interface, None)
    if not counter:
        print(f'{interface} is not found')
        os._exit(0)
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [
            (now - last) / (t1 - t0) / 1000.0
            for now, last in zip(tot, last_tot)
        ]
        rate.append((ul, dl))
        t0 = time.time()
        time.sleep(dt)


def print_rate(rate):
    try:
        print("Ul: {0:.0f} kB/s    Dl: {1:.0f} kB/s ".format(*rate[-1]) + ' ' * 20, end='\r', flush=True)
    except IndexError:
        "Ul: - kB/s/ Dl: - kB/s"


def main():
    parser = ArgumentParser()
    parser.add_argument('--interface', '-i', type=str, default='', help='network interface (eth0/en0)')
    args = parser.parse_args()
    interface = args.interface
    if not interface:
        if 'macos' in platform.platform().lower():
            interface = 'en0'
        else:
            interface = 'eth0'

    # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
    transfer_rate = deque(maxlen=1)
    t = threading.Thread(target=calc_ul_dl, args=(transfer_rate, time_interval, interface))
    # The program will exit if there are only daemonic threads left.
    t.daemon = True
    t.start()

    # The rest of your program, emulated by me using a while True loop
    while True:
        print_rate(transfer_rate)
        time.sleep(time_interval)


if __name__ == '__main__':
    main()
