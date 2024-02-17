import network
import socket
import time
import struct
import machine
import gc

NTP_DELTA = 2208988800
host = "pool.ntp.org"

class timeSync:
    @staticmethod
    def set_time():
        try:
            NTP_QUERY = bytearray(48)
            NTP_QUERY[0] = 0x1B
            addr = socket.getaddrinfo(host, 123)[0][-1]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.settimeout(1)
                res = s.sendto(NTP_QUERY, addr)
                msg = s.recv(48)
            finally:
                s.close()
            
            val = struct.unpack("!I", msg[40:44])[0]
            t = val - NTP_DELTA    
            tm = time.gmtime(t)
            machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            
            # (year, month, mday, hour, minute, second, weekday, yearday)
            print("Time set to: {day:02d}.{month:02d}.{year:04d}, {hour:02d}:{minute:02d}:{second:02d}, weekday: {weekday:01d}, yearday: {yearday:03d}".format(day=tm[2], month=tm[1], year=tm[0], hour=tm[3], minute=tm[4], second=tm[5], weekday=tm[6], yearday=tm[7]))
            
            #print("Time set to: {day:02d}.{month:02d}.{year:04d}, {hour:02d}:{minute:02d}:{second:02d}.format(day=tm[2], month=tm[1], year=tm[0], hour=tm[3], minute=tm[4], second=tm[5]))
            #print("time set to: " + str(tm[2]) + "." + str(tm[1]) + "." + str(tm[0]) + ", " + str(tm[3]) + ":" + str(tm[4]) + ":" + str(tm[5]))
        except OSError as exc:
            if exc.args[0] == 110: #ETIMEDOUT
                time.sleep(2)
                pass

    @staticmethod
    def convertTimestamp(timestampStr):
        # 2022-10-27T03:47:44+00:00
        dateStr = timestampStr.split("T")[0]
        timeStr = timestampStr.split("T")[1]
        
        year = dateStr.split("-")[0]
        month = dateStr.split("-")[1]
        day = dateStr.split("-")[2]
        
        timeStr = timeStr.split("+")[0]
        hour = timeStr.split(":")[0]
        minute = timeStr.split(":")[1]
        second = timeStr.split(":")[2]
        
        # (year, month, mday, hour, minute, second, weekday, yearday)
        return (int(year), int(month), int(day), int(hour), int(minute), int(second), 0, 0)
    
    
    