import socket
import requests

def get_external_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    return ip

# https://stackoverflow.com/a/28950776
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable, is a broadcast address anyway
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP