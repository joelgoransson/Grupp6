import bluetooth, subprocess
from flask import Flask, render_template, redirect
from flask_script import Manager, Server

def connect():
	nearby_devices = bluetooth.discover_devices(duration=4,lookup_names=True, flush_cache=True, lookup_class=False)
	print("Which would would you like to connect to?")
	for index, device in enumerate(nearby_devices, start=1):
		print(str(index) + ":", device)

	select = int(input("Select:" ))
	print("Connecting to ", nearby_devices[select - 1][1])
	global sock, bd_addr, port
	bd_addr = nearby_devices[select - 1][0]
	port = 1
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bd_addr,port))

def led_on():
	global sock
	print("1 sent")
	sock.send("1".encode())

def led_off():
	global sock
	print("0 sent")
	sock.send("0".encode())

def get_status():
	global sock
	sock.send("2".encode())
	print("SENT 2")
	data = sock.recv(1).decode()
	print("DATA:", data)
	return data

class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        connect()
        return Server.__call__(self, app, *args, **kwargs)

app = Flask(__name__)
manager = Manager(app)
manager.add_command('runserver', CustomServer())


@app.route('/')
def index(name=None):
	status = get_status()
	return render_template("index.html", status=status, name=name)

@app.route('/off/')
def off(name=None):
	led_off()
	return redirect("/")

@app.route('/on/')
def on(name=None):
	led_on()
	return redirect("/")

if __name__ == "__main__":
    manager.run()
