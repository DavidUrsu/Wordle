from multiprocessing.connection import Listener

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()
print ("connection accepted from" + str(listener.last_accepted))
msg = conn.recv()
print(msg)
listener.close()