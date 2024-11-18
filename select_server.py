# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen()
    set = [s]
    while True:
        ready_sockets, _, _ = select.select(set, [], [])
        for notified_socket in ready_sockets:
            if notified_socket is s: # listening socket
                conn, addr = s.accept()
                set.append(conn)
                print(addr, ": connected")
            else: # client socket
                data = notified_socket.recv(1024)
                if not data: # client disconnected
                    set.remove(notified_socket)   
                    print(notified_socket.getpeername(), ": disconnected")
                    notified_socket.close()
                    continue
                print(f"{notified_socket.getpeername()} {len(data)} bytes: {data}")
                # notified_socket.sendall(data)

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
