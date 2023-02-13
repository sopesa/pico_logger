import network
import socket
from time import sleep
from picozero import pico_temp_sensor
import machine
import binascii


ssid = 'ssid'
password = 'password'

led = machine.Pin("LED", machine.Pin.OUT)

# Function for led blinking used for feedback
def cute_blink():
    led.off()
    for i in range(5):
        led.toggle()
        sleep(0.1)
    led.off()

# Function for connecting to a WiFi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    i=0
    networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
    for w in networks:
        i+=1
        print(i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5])
    
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Connecting...')
        led.toggle()
        sleep(1)
    led.off()
    cute_blink()
    print(wlan.ifconfig()[0])
    return wlan.ifconfig()[0]
    
# Function for disconnecting from a connected WiFi and turn the WiFi off on the Pico
def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)
    while wlan.isconnected() != False:
        print('Disconnecting...')
        led.toggle()
        sleep(1)
    cute_blink()

# Function for opening a socket on the Pico
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>

            <body> 
                <form action="./lighton">
                    <input type="submit" value="Light on" />
                </form>

                <form action="./lightoff">
                    <input type="submit" value="Light off" />
                </form>
                <p>LED:  {state}</p>
                <p>Temp: {temperature}</p>
            </body>

            </html>
            """
    return str(html)

def serve(connection):
    state = "OFF"
    led.on()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led.on()
            state = 'ON'
        elif request == '/lightoff?':
            led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    # uncomment and run script to disconnect form WiFi
    # disconnect()
except Exception:
    print('Error!');