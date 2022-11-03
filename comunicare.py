from multiprocessing.connection import Listener, Client

address = ('localhost', 6000)

def trimitere(data):
    conn = Client(address, authkey=b'secret password')
    conn.send(data)
    conn.close()

def primire():
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    data = conn.recv()
    listener.close()
    return data