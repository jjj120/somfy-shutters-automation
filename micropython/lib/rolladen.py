from machine import Pin
import uasyncio


class Rolladen:
    def __init__(self, lower_time=28.0, raise_time=30.0, raise_offset=8.0):
        self.upPin = Pin(20, Pin.OUT, Pin.PULL_DOWN)
        self.upPin.value(1)
        self.myPin = Pin(19, Pin.OUT, Pin.PULL_DOWN)
        self.myPin.value(1)
        self.downPin = Pin(18, Pin.OUT, Pin.PULL_DOWN)
        self.downPin.value(1)
        self.progPin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
        self.progPin.value(1)

        self.lower_time = lower_time
        self.raise_time = raise_time
        self.raise_offset = raise_offset

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

    async def set_to(self, percent: float):
        if percent < 0 or percent > 100:
            raise ValueError("Percentage must be between 0 and 100")
        if percent == 0:
            await self.lower_()
        elif percent == 100:
            await self.raise_()
        else:
            await self.raise_()
            await uasyncio.sleep_ms(
                (self.raise_offset + self.raise_time) * 1000
            )  # wait for the rolladen to be fully raised

            # calculate the time the rolladen should be lowered
            time_to_lower = self.lower_time * percent / 100

            await self.lower_()
            await uasyncio.sleep_ms(int(round(time_to_lower * 1000)))
            await self.stop()

    async def toggle(self):
        if self.raised:
            uasyncio.create_task(self.lower_())
        else:
            uasyncio.create_task(self.raise_())
        print("Toggled")
