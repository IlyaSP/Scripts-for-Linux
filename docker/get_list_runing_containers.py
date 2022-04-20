import docker
import socket
from contextlib import closing
import sys


def check_status_containers(etalon):
    status = "OK"
    contaners_list = []
    client = docker.from_env()    # Подключенеи к сокету докер
    contaners = client.containers.list(filters={'status' : 'running'})    # Получаем список запущенных контейнеров
    for i in contaners:
      contaners_list.append(i.name)    # Формируем список запущенных контейнеров
    contaners_set = set(contaners_list)
    contaner_not_run = etalon.difference(contaners_set)    # Сравиниваем список запущенных контенеров с эталонным
    if len(contaner_not_run) != 0:
        status = "FAILED"
    return status, contaner_not_run

def check_socket(hosts, ports):
    inaccessible_ports = []
    for host in hosts:
        for port in ports:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex((host, int(port))) != 0:
                    inaccessible_ports.append("{0}:{1}".format(host, port))
                else:
                    continue
    return inaccessible_ports


if __name__ == "__main__":
    etalon = {"portainer", "gitlab-runner", "gitlab"}
    etalon_ports = ["443", "7777"]
    hosts = ["192.168.56.7"]
    status, contaner_not_run = check_status_containers(etalon)
    if status == "FAILED":
        print ("FAILED check running contaners")
        for i in contaner_not_run:
            print ("container '{0}' not running".format(i))
        sys.exit(1)
    elif status == "OK":
        print("All contaners is running")
    inaccessible_ports = check_socket(hosts, etalon_ports)
    if len(inaccessible_ports) != 0:
        print("FAILED check open ports")
        for i in inaccessible_ports:
            print("port on '{0}' inaccessible".format(i))
        sys.exit(1)
    elif len(inaccessible_ports) == 0:
        print("All ports are available")
