try:
 import usocket as socket
except:
 import socket
import network
import gc
from machine import Pin
import time as t

#BM 1
In1=Pin(6,Pin.OUT) 
In2=Pin(7,Pin.OUT)  
EN_A=Pin(8,Pin.OUT)

#BM 2
In3=Pin(4,Pin.OUT)  
In4=Pin(3,Pin.OUT)  
EN_B=Pin(2,Pin.OUT)

#FM 1
In11=Pin(19,Pin.OUT) 
In22=Pin(20,Pin.OUT)  
EN_AA=Pin(21,Pin.OUT)

#FM 2
In33=Pin(18,Pin.OUT) 
In44=Pin(17,Pin.OUT)  
EN_BB=Pin(16,Pin.OUT)

EN_A.high()
EN_B.high()
EN_AA.high()
EN_BB.high()

gc.collect()
ssid = 'Pico'           
password = 'PIC0TEST'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
    pass
print('Connection is successful')
print(ap.ifconfig())

def frwrd():
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    In11.low()
    In22.high()
    In33.high()
    In44.low()
    print("Forward")
    
def bckwrd():
    In1.high()
    In2.low()
    In3.low()
    In4.high ()
    In11.high()
    In22.low()
    In33.low()
    In44.high()  
    print("Backward")
    
def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()
    In11.low()
    In22.low()
    In33.low()
    In44.low()
    print("Stop")
    
def left():
    print("Left")
    
def right():
    print("Right")

def webpage():
    html = f"""
            <!DOCTYPE html>
                <html>
                    <head>
                        <title>Pico Connectivity Test</title>
                    </head>
                    <center><b>
                    <form action="./forward">
                        <input type="submit" value="Forward" style="height:120px; width:120px; color:lightblue; border-radius:20px; border-color:lightblue; background:white; font-size:24px; font-weight:bold"/>
                    </form>
                    <table><tr>
                    <td><form action="./left">
                        <input type="submit" value="Left" style="height:120px; width:120px; color:lightblue; border-radius:20px; border-color:lightblue; background:white; font-size:24px; font-weight:bold" />
                    </form></td>
                    <td><form action="./stop">
                        <input type="submit" value="Stop" style="height:120px; width:120px; color:lightblue; border-radius:20px; border-color:lightblue; background:white; font-size:24px; font-weight:bold" />
                    </form></td>
                    <td><form action="./right">
                        <input type="submit" value="Right" style="height:120px; width:120px; color:lightblue; border-radius:20px; border-color:lightblue; background:white; font-size:24px; font-weight:bold" />
                    </form></td>
                    </tr></table>
                    <form action="./back">
                        <input type="submit" value="Back" style="height:120px; width:120px; color:lightblue; border-radius:20px; border-color:lightblue; background:white; font-size:24px; font-weight:bold" />
                    </form>
                    </body>
                </html>
            """
    return str(html)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    #print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    try:
        request = request.split()[1]
    except IndexError:
        pass
    if request == '/forward?':
        frwrd()
    elif request =='/left?':
        left()
    elif request =='/stop?':
        stop()
    elif request =='/right?':
        right()
    elif request =='/back?':
        bckwrd()
    response = webpage()
    conn.send(response)
    conn.close()
