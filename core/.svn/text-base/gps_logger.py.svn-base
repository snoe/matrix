import time
from threading import Thread
import Queue
import lib.gps
from datetime import date, datetime
from logger import log
import socket
import copy

qout = Queue.Queue()
qcmd = Queue.Queue()

class GPS(object):
    def __init__(self, gpsfile):
        self.reset()
        self.poller = Poller(gpsfile)
        self.poller.start()
    
    def reset(self, *args):
        self.trip_start = datetime.now()
        self.total_speed = 0
        self.fixes = []
        self.fix = None
        qcmd.put("RESET")

    # synchs to the poller
    def synch(f):
        def _inner(self, *args, **kwargs):
            fix = None
            while not qout.empty():
                fix = qout.get_nowait()
                self.fixes.append(fix)
                self.total_speed += fix.speed
                
                
            self.fix = fix

            return f(self)
        return _inner

    def close(self):
        qcmd.put("SHUTDOWN")

    def get_trip_time(self):
        return datetime.now() - self.trip_start

    @synch
    def get_total_distance(self):
        d = 0
        for i in xrange(0, len(self.fixes)-1, 2):
            f1 = self.fixes[i]
            f2 = self.fixes[i+1]
            d += lib.gps.EarthDistance((f1.latitude, f1.longitude), (f2.latitude, f2.longitude))
        return d/1000.0 # in km

    @synch
    def get_speed(self):
        if self.fix:
            mps = self.fix.speed
            kmh = mps * 3.6
            return kmh
        else:
            return None

    @synch
    def get_avg_speed(self):
        if self.fixes:
            avg_mps = self.total_speed / len(self.fixes)
            return avg_mps * 3.6
        else:
            return 0

class Poller(Thread):
    def __init__(self, gpsfile):
        Thread.__init__(self)
        self.gpsfile = gpsfile
        self.data_reset()
        
        self.session = None
        try:
            self.gps_poll()
        except:
            self.session = None

    def data_reset(self):        
        self.readings = []        
        self.today = date.today()

    def save(self):
        if self.readings:
            ofile = self.gpsfile + self.today.strftime("%Y-%m-%d")
            f = open(ofile, "wb")
            f.writelines(self.readings)

        if self.today != date.today():
            self.data_reset()

    def reset(self):
        if self.readings:
            ofile = self.gpsfile + datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            f = open(ofile, "ab")
            f.writelines(self.readings)

        self.data_reset()

    def gps_poll(self):
        if not self.session:
            try:
                self.session = lib.gps.gps()
            except socket.error, e:
                print "cannot connect"
                raise e

        try:
            self.session.query('o')
        except socket.error, e:
            print "cannot query"
            self.session.close()
            self.session = None
            raise e

    def run(self):
        while True:
            time.sleep(1)

            while not qcmd.empty():
                cmd = qcmd.get_nowait()
                if cmd == "RESET":
                    self.reset()
                if cmd == "SHUTDOWN":
                    self.save()
                    return
                    
            try:
                self.gps_poll()
            except:
                continue
            
            if self.session.fix.mode != lib.gps.MODE_NO_FIX and self.session.fix.speed != lib.gps.NaN:
                qout.put(copy.copy(self.session.fix))
                self.readings.append(self.session.response)
                if len(self.readings) % 30 == 0:
                    self.save()
