#!/usr/bin/env python

from flask import Flask, jsonify
from pyaxidraw import axidraw

app = Flask(__name__)

cmd_table = {
    'mt': [ 'moveto', [float, float] ],
    'lt': [ 'lineto', [float, float] ],
    'pu': [ 'penup',[] ],
    'pd': [ 'pendown',[] ]
}
# Global device connection (initialize it at startup)
device_connection = None

def create_device_connection():
    global device_connection
    if device_connection is None:
        print("Opening connection to the device...")
        device_connection = axidraw.AxiDraw()
        device_connection.options.port = "/dev/ttyACM0"
        device_connection.interactive()
        if not device_connection.connect():            
        	print("not found")
        	quit()
    return device_connection

# Route to access the device
@app.route('/cmd/<cmd>')
@app.route('/cmd/<cmd>/<options>')
def device_cmd(cmd,options=None):
    if cmd in cmd_table:
        axi_cmd   = cmd_table[cmd][0]
        if options:
            axi_types = cmd_table[cmd][1]
            cmd_list  = [a.strip() for a in options.split(',')]
            args      = [z[1](z[0]) for z in zip(cmd_list, axi_types)]
            getattr(device_connection, axi_cmd)(*args)
        else:
            print("command no options", axi_cmd)
            getattr(device_connection, axi_cmd)()
        
    return f"{cmd},{options}"

@app.route('/connect')
def connect_device():
    create_device_connection()
    return "Connected to Device"


@app.route('/disconnect')
def device_shutdown():
    device_connection.disconnect()
    devince_connection = None
    return "Disconnected from Device"
    
if __name__ == '__main__':
    create_device_connection()
    app.run(debug=True, port=9090,host="0.0.0.0")
