import time
import network


class wlan:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
    
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        # Wait for connect or fail
        max_wait = 30
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print(str(self.wlan.status()) + " - Waiting for connection")
            time.sleep(1)

        # Handle connection error
        if self.wlan.status() != 3:
            self.wlan.disconnect()
            raise RuntimeError("network connection failed")
        else:
            print("Connection successful")
            status = self.wlan.ifconfig()
            print("IP: " + status[0])



    def disconnect(self):
        self.wlan.disconnect()