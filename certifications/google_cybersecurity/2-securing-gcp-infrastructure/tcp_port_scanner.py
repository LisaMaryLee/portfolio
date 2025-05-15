# tcp_port_scanner.py

import socket

def scan_ports(host, ports):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    target = "127.0.0.1"
    ports = range(20, 1025)
    print(f"Scanning {target}...")
    found = scan_ports(target, ports)
    print("Open ports:", found)
