import urequests, ujson, time, gc
from timeSync import TimeSync

class Sun():
    def __init__(self, telegram_token, retries=5, retryTime=0.1, twilight="civil"):
        self.TOKEN = telegram_token
        requestTelegram = urequests.get("https://api.telegram.org/bot{TOKEN}/sendMessage?text=Started sun class&chat_id=5411292173".format(TOKEN=self.TOKEN))
        requestTelegram.close()
        self.retries = retries
        self.retryTime = retryTime #seconds
        self.recursionCounter = 0
        self.twilight = twilight
        self.currSet = False
        
        self.rise = (2022, 1, 1, 0, 0, 0, 0, 0)
        self.set  = (2022, 1, 1, 0, 0, 0, 0, 0)
        
        self.refresh()
    
    def refresh(self):
        self.currSet = False
        #https://api.sunrise-sunset.org/json?lat=48.15412112450283&lng=16.306680813206004&date=today
        
        """
        {
            "results":
                {
                    "solar_noon": "2015-05-21T12:14:17+00:00",
                    "day_length": 51444,
                    "sunrise": "2015-05-21T05:05:35+00:00",
                    "sunset":  "2015-05-21T19:22:59+00:00",
                    "civil_twilight_begin": "2015-05-21T04:36:17+00:00",
                    "civil_twilight_end":   "2015-05-21T19:52:17+00:00",
                    "nautical_twilight_begin": "2015-05-21T04:00:13+00:00",
                    "nautical_twilight_end":   "2015-05-21T20:28:21+00:00",
                    "astronomical_twilight_begin": "2015-05-21T03:20:49+00:00",
                    "astronomical_twilight_end":   "2015-05-21T21:07:45+00:00"
                },
            "status":"OK"
        }
        """
        
        
        if not (self.twilight == "civil" or self.twilight == "nautical" or self.twilight == "astronomical"):
            raise Exception("False twilight type! (Choose from: civil, nautical, astronomical")
        
        gc.collect()
        try:
            request = urequests.get("https://api.sunrise-sunset.org/json?lat=48.15412112450283&lng=16.306680813206004&date=today&formatted=0")
            sunData = ujson.loads(request.text)
            request.close()
            
            if sunData["status"] != "OK":
                if self.recursionCounter >= self.retries:
                    raise ConnectionError("could not connect to sunset api")
                else:
                    self.recursionCounter += 1
                    time.sleep(self.retryTime)
                    return self.refresh()
            
            self.recursionCounter = 0

        except OSError as err:
            #if err.errno == 103:
            requestTelegram = urequests.get("https://api.telegram.org/bot{TOKEN}/sendMessage?text=Sunset API is down or can't be reached&chat_id=5411292173".format(TOKEN=self.TOKEN))
            requestTelegram.close()
            return self.rise, self.set
            
        
        # (year, month, mday, hour, minute, second, weekday, yearday)
        self.rise = TimeSync.convertTimestamp(sunData["results"][self.twilight + "_twilight_begin"])
        self.set  = TimeSync.convertTimestamp(sunData["results"][self.twilight + "_twilight_end"])
        
        self.currSet = True
        return self.rise, self.set
        

    @property
    def get_sunrise(self):
        self.refresh()
        return self.rise
    
    @property
    def get_sunset(self):
        self.refresh()
        return self.set