#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import ipaddress
import logging
import socket
import sys
import time

TIMEOUT = 3  # timeout value in seconds

def tcp_handshake(host, port):
    """
    Check TCP handshake connection

    Parameters
    ----------
    host : str
        Destination host ipv4 address
    port : int
        Destination port number

    Returns
    -------
    True if TCP handshake is successful, False if not.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    try:
        ipaddress.IPv4Network(host)
    except ValueError:
        logging.error('ip address is not correct format.{0}'.format(host))
        sys.exit(1)
    
    success = False
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        success = True
    except socket.timeout:
        pass
    except OSError as e:
        logging.error('OS error: {0}'.format(e))
        sys.exit(2)
    except Exception as e:
        logging.error('Unexpected error: {0}'.format(e))
        sys.exit(3)

    return success, s.getsockname()


if __name__ == '__main__':
    
    if len(sys.argv) != 4:
        print('Usage: {0} <destination ip address> <destination port> <output.csv>'.format(sys.argv[0]))
        sys.exit(0)
    try:
        count = 0
        while True:
            success, (client_ip, client_port) = tcp_handshake(sys.argv[1], sys.argv[2])
            result = 'success' if success else 'fail'

            # please comment out to get the standard output
            # print('TCP connection to {0} is {1} on {2} from port {3}.'
            #       .format(sys.argv[1], result, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), client_port))
            
            row = ','.join([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                sys.argv[1], # destination ip address
                sys.argv[2], # destination port
                str(client_port), 
                result,
                '\n'
            ])
            try:
                with open(sys.argv[3], 'a') as f:
                    f.write(row)
            except IOError as e:
                logging.error('IO error: {0}'.format(e))
                sys.exit(9)
            count += 1
            print(f'Opening a TCP Handshake to {sys.argv[1]}:{sys.argv[2]} every 1 seconds...executed {count} times.')
            time.sleep(1)
    except KeyboardInterrupt:
        pass

