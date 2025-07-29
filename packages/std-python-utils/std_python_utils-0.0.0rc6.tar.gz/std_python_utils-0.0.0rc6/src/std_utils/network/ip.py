import importlib
import socket
from contextlib import contextmanager
from typing import Final, Literal

import requests


ip_check_url: Final[str] = 'https://ifconfig.me'


def force_ipv6(host, port, family=0, type=0, proto=0, flags=0):
    return [(socket.AF_INET6, socket.SOCK_STREAM, 6, '', (host, port))]


def force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (host, port))]


ip_ver_to_socket_func = {
    4: force_ipv4,
    6: force_ipv6
}


def get_ip(ip_ver: Literal[4, 6]):
    old_getaddrinfo = socket.getaddrinfo
    socket.getaddrinfo = ip_ver_to_socket_func[ip_ver]
    try:
        response = requests.get(ip_check_url)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Request failed to get ipv{ip_ver} address: {ip_check_url}: {e}")
    finally:
        socket.getaddrinfo = old_getaddrinfo


def get_ip4_ip6_tuple():
    return get_ip(4), get_ip(6)


@contextmanager
def ipv6():
    importlib.reload(socket)
    old_getaddrinfo = socket.getaddrinfo
    try:
        socket.getaddrinfo = force_ipv6
        yield
    finally:
        socket.getaddrinfo = old_getaddrinfo


@contextmanager
def ipv4():
    importlib.reload(socket)
    old_getaddrinfo = socket.getaddrinfo
    try:
        socket.getaddrinfo = force_ipv4
        yield
    finally:
        socket.getaddrinfo = old_getaddrinfo
