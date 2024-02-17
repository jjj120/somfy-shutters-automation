from machine import Pin
import uasyncio

class Rolladen:
    def __init__(self):
        self.upPin   = Pin(20, Pin.OUT, Pin.PULL_DOWN)
        self.upPin.value(1)
        self.myPin   = Pin(19, Pin.OUT, Pin.PULL_DOWN)
        self.myPin.value(1)
        self.downPin = Pin(18, Pin.OUT, Pin.PULL_DOWN)
        self.downPin.value(1)
        self.progPin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
        self.progPin.value(1)
        
        self.raised = False
        self.led = Pin("LED", Pin.OUT)
        
    
    async def raise_(self):
        self.upPin.value(0)
        await uasyncio.sleep_ms(50)
        self.upPin.value(1)
        
        self.raised = True
        self.led.value(1)
        print("Raised")
        return
    
    
    async def lower_(self):
        self.downPin.value(0)
        await uasyncio.sleep_ms(50)
        self.downPin.value(1)
        
        self.raised = False
        self.led.value(0)
        print("Lowered")
        return
    
    async def stop(self):
        self.myPin.value(0)
        await uasyncio.sleep_ms(50)
        self.myPin.value(1)
        
        print("Stopped")
        return
    
    async def toggle(self):
        if self.raised:
            uasyncio.create_task(self.lower_())
        else:
            uasyncio.create_task(self.raise_())
        print("Toggled")

