import time

from gravity_controller_operator.controllers_super import DIInterface, RelayInterface, ControllerInterface
from _thread import allocate_lock
from socket import socket


class SigurBase:
    def __init__(self, sock):
        self.sock = sock
        self.mutex = allocate_lock()
        self.login()
        self.subscribe_ce()

    def login(self, login="Administrator", password=""):
        return self._send_command(f'"LOGIN" 1.8 "{login}" "{password}"')

    def subscribe_ce(self):
        return self._send_command(f'"SUBSCRIBE" CE')

    def _send_command(self, command, get_response=True):
        time.sleep(0.3)
        self.mutex.acquire()
        command = f'{command}\r\n'
        self.sock.send(command.encode("utf-8"))
        if get_response:
            response = self.sock.recv(1024)
            self.mutex.release()
            return response
        self.mutex.release()


class SigurDI(DIInterface, SigurBase):
    map_keys_amount = 5
    starts_with = 3

    def __init__(self, sock):
        SigurBase.__init__(self, sock)
        DIInterface.__init__(self)

    def get_phys_dict(self):
        result = {}
        for point in range(self.starts_with, self.starts_with + self.map_keys_amount):
            raw = self._send_command(f'"GETAPINFO" {point}')
            response = raw.decode()
            status = response.split(" ")[-2]
            result[point] = status
        return result


class SigurRelay(RelayInterface, SigurBase):
    map_keys_amount = 3
    starts_with = 1

    def __init__(self, sock):
        SigurBase.__init__(self, sock)
        RelayInterface.__init__(self)

    def get_phys_dict(self):
        result = {}
        for point in range(self.starts_with, self.starts_with + self.map_keys_amount):
            raw = self._send_command(f'"GETAPINFO" {point}')
            response = raw.decode()
            status = response.split(" ")[-2]
            result[point] = status
        return result

    def change_phys_relay_state(self, addr, state: bool):
        # Имитация действия, при необходимости можно добавить настоящую команду
        pass


class Sigur:
    model = "sigur"

    def __init__(self, sock, login="Administrator", password="",
                 name="Sigur", *args, **kwargs):
        di = SigurDI(sock)
        relay = SigurRelay(sock)
        self.interface = ControllerInterface(di_interface=di, relay_interface=relay)
