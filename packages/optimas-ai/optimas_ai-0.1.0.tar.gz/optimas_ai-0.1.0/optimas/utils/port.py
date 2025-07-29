import socket

def find_available_port(start_port=56430, port_range=100):
    """Finds an available port by attempting to bind a socket."""
    for port in range(start_port, start_port + port_range):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result != 0:  # Port is available
                return port
    raise Exception("No available port found in the specified range.")
