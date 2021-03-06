import socket
import json
import requests
import pickle
import time

def check_tunnel_ports(ports):
    print("socket ports: {}".format(ports))
    tp = []
    for port in ports:
        try:
            r = requests.get("http://{}:{}".format(socket.gethostbyname('sshd'), port))
            if r.ok:
                tp.append(int(port))
        except Exception as e:
            print("exception: {}".format(e))
            print("except: {}".format(port))
            pass
    print("checked ports: {}".format(tp))
    return tp

def get_tunnel_ports():
    data = {'get':'active_tunnel_ports'}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('sshd', 3773))
    s.send(json.dumps(data))
    ports = []
    while 1:
        rdata = s.recv(8192)
        if rdata:
            ports.append(check_tunnel_ports(json.loads(rdata)))
        else:
            break
            break
    s.close()
    return ports

while True:
    pickle.dump(get_tunnel_ports(), open("/tmp/active_tunnel_ports","wb"))
    time.sleep(10)

