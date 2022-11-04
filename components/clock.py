import math
import datetime
import time

from utils import debugShow


class Clock:

    def __init__(self, io_ports_for_clock):
        self.__hourNow = datetime.datetime.now().time().hour
        self.__minuteNow = datetime.datetime.now().time().minute
        self.__secondNow = datetime.datetime.now().time().second
        self.__IoPorts = io_ports_for_clock
        self.startClock()

    def startClock(self):
        while 1:
            temp_hours = self.__IoPorts[self.__hourNow % 12]
            if not self.__IoPorts[self.__hourNow % 12].isLightOn():
                self.__IoPorts[self.__hourNow % 12].lightOn()
            if self.__hourNow % 12 != math.floor(self.__minuteNow / 5):
                self.__IoPorts[math.floor(self.__minuteNow / 5)].lightOn()
            debugShow(self.__IoPorts)
            time.sleep(0.5)
            if self.__hourNow % 12 != math.floor(self.__minuteNow / 5):
                self.__IoPorts[math.floor(self.__minuteNow / 5)].lightOff()
            debugShow(self.__IoPorts)
            time.sleep(0.5)
            self.__minuteNow = datetime.datetime.now().time().minute
            self.__hourNow = datetime.datetime.now().time().hour
            if self.__IoPorts[self.__hourNow % 12].get() != temp_hours.get():
                temp_hours.lightOff()
