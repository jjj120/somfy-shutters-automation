import time, machine, uasyncio
from sched.sched import schedule
from microdot_asyncio import Microdot, redirect

from wlan import wlan
from rolladen import Rolladen
from timeSync import timeSync
from sun import sun
from config import WIFI_SSID, WIFI_PASSWORD


#init wlan instance and connect to wlan
wlan = wlan(WIFI_SSID, WIFI_PASSWORD)
wlan.connect()

#sync time with ntp server
timeSync.set_time()

#init sun instance and get data from api
sun = sun()

#inti rolladen obj
rolladen = Rolladen()

#print current time
print(time.gmtime())


#---------------------------------------------------------------------------------------
sunsetTask = 0
sunriseTask = 0


#define keywordless functions for use with schedule

async def syncTime():
    #run every 2 hours
    timeSync.set_time()

async def sunsetFunction():
    #run every day at sunset
    uasyncio.create_task(rolladen.lower_())

async def sunriseFunction():
    #run every day at sunset
    #uasyncio.create_task(rolladen.raise_())
    await uasyncio.sleep(0.5)

async def refreshSun():
    #run every day at 2am
    
    global sunsetTask, sunriseTask
    sun.refresh()
    
    
    #renew sunset and sunrise task time
    
    #cancel prev sunset task:
    try: sunsetTask.cancel()
    except Exception as e: print(e)
    
    #create new sunset task
    # (year, month, mday, hour, minute, second, weekday, yearday)
    sunset = sun.set
    sunsetTask = uasyncio.create_task(schedule(sunsetFunction, month=sunset[1], mday=sunset[2], hrs=sunset[3], mins=sunset[4], secs=sunset[5]))
    
    
    #cancel prev sunrise task:
    try: sunriseTask.cancel()
    except Exception as e: print(e)
    
    #create new sunrise task
    # (year, month, mday, hour, minute, second, weekday, yearday)
    sunrise = sun.rise
    sunriseTask = uasyncio.create_task(schedule(sunriseFunction, month=sunrise[1], mday=sunrise[2], hrs=sunrise[3], mins=sunrise[4], secs=sunrise[5]))
    


#---------------------------------------------------------------------------------------
#webserver:
app = Microdot()

@app.route("/")
async def mainPage(request):
    sunrise = sun.rise
    sunset = sun.set
    timeNow = time.gmtime()
    
    timeString = "{mday:02d}.{month:02d}.{year:04d}, {hour:02d}:{minute:02d}:{second:02d}".format(year=timeNow[0], month=timeNow[1], mday=timeNow[2], hour=timeNow[3], minute=timeNow[4], second=timeNow[5])
    
    # (year, month, mday, hour, minute, second, weekday, yearday)
    sunriseStr = "{mday:02d}.{month:02d}.{year:04d}, {hour:02d}:{minute:02d}:{second:02d}".format(year=sunrise[0], month=sunrise[1], mday=sunrise[2], hour=sunrise[3], minute=sunrise[4], second=sunrise[5])
    sunsetStr  = "{mday:02d}.{month:02d}.{year:04d}, {hour:02d}:{minute:02d}:{second:02d}".format(year=sunset[0],  month=sunset[1],  mday=sunset[2],  hour=sunset[3],  minute=sunset[4],  second=sunset[5])
    
    sunriseSetStr = "<p><b>Sunrise:</b> {sunrise}</p><p><b>Sunset:</b>  {sunset}</p>".format(sunrise=sunriseStr, sunset=sunsetStr)
    
    if rolladen.raised:
        raisedStr = "oben."
        buttonStr = """
            <a href="/lower">
                <button style="width: 100%">Schlie&szlig;en</button>
            </a>
        """
    else:
        raisedStr = "unten."
        buttonStr = """
        <a href="/raise">
            <button style="width: 100%">&Ouml;ffnen</button>
        </a>
        """
    

    htmlString = startPage.format(raisedStr=raisedStr, sunriseSetStr=sunriseSetStr, timeString=timeString)
    
    return htmlString, {'Content-Type': 'text/html'}

@app.route("/raise")
async def raiseLaden(request):
    uasyncio.create_task(rolladen.raise_())
    return redirect("/")
    

@app.route("/lower")
async def lowerLaden(request):
    uasyncio.create_task(rolladen.lower_())
    return redirect("/")

@app.route("/stop")
async def stopLaden(request):
    uasyncio.create_task(rolladen.stop())
    return redirect("/")

@app.route("/toggle")
async def toggleLaden(request):
    uasyncio.create_task(rolladen.toggle())
    return redirect("/")

@app.route("/refresh")
async def refreshTasks(request):
    uasyncio.create_task(refreshSun())
    return redirect("/")
    

@app.route("/sunrise")
async def callSunriseTask(request):
    uasyncio.create_task(sunriseFunction())
    return redirect("/")

@app.route("/sunset")
async def callSunsetTask(request):
    uasyncio.create_task(sunsetFunction())
    return redirect("/")



#---------------------------------------------------------------------------------------

def start_server():
    print('Starting microdot app')
    try:
        app.run(port=80)
    except:
        app.shutdown()



#start async tasks
print("starting async tasks")

async def main():
    global refreshSunTask, timeSyncTask
    refreshSunTask = uasyncio.create_task(schedule(refreshSun, hrs=2))
    timeSyncTask = uasyncio.create_task(schedule(syncTime, hrs=range(0, 24, 2)))
    
    await start_server()

uasyncio.run(main())

#---------------------------------------------------------------------------------
#cleanup
machine.Pin("LED").value(0)

wlan.disconnect()
uasyncio.new_event_loop()
