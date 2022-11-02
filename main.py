# import RPi.GPIO as IO
import datetime
import sys
import getopt
import threading

import time

ioPorts = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]
groundPorts = [6, 9, 14, 20, 25, 30, 34, 39]
uselessPorts = [1, 2, 4, 17, 27, 28]
inUsePorts = []

allPorts = set(ioPorts)
allPorts.update(groundPorts)
allPorts.update(uselessPorts)


def check():
    if len(allPorts) != 40:
        print("ААААААААААА ПЛАТА ГОРИТ ТУШИ (Count)\n")
        exit(1)
    if len(ioPorts) != 26 or len(groundPorts) != 8 or len(uselessPorts) != 6:
        print("ААААААААААА ПЛАТА ГОРИТ ТУШИ (IO)\n")
        exit(1)


class IoPort(object):
    def __init__(self, numPort):
        if (numPort not in ioPorts) or (numPort in inUsePorts):
            print("ПОРТ НЕПРАВИЛЬНО УКАЗАН ВСЁ СГОРИТ (Init)\n")
            exit(2)
        self.__ioPort = numPort
        self.__voltage = 0
        inUsePorts.append(numPort)
        self.__lock = threading.Lock()
        # IO.setup(self.__ioPort, IO.OUT)
        # IO.output(self.__ioPort, self.__voltage)

    def get(self):
        if not (self.__ioPort in inUsePorts):
            print("ПОРТ НЕПРАВИЛЬНО УКАЗАН ВСЁ СГОРИТ (Get)\n")
            exit(2)
        return self.__ioPort

    def lightOn(self):
        self.__lock.acquire()
        try:
            if self.__voltage == 1:
                print('Два раза зажгли одно и то же!!!\n')
                exit(3)
            self.__voltage = 1
            # print('Порт номер ', self.__ioPort, ' светится\n')
            # IO.output(self.__ioPort, self.__voltage)
        finally:
            self.__lock.release()

    def lightOff(self):
        self.__lock.acquire()
        try:
            if self.__voltage == 0:
                print('Два раза выключили одно и то же!!!\n')
                exit(3)
            self.__voltage = 0
            # print('Порт номер ', self.__ioPort, ' мрак\n')
        # IO.output(self.__ioPort, 0)
        finally:
            self.__lock.release()

    def isLightOn(self):
        return self.__voltage == 1

    def inverse(self):
        self.__lock.acquire()
        try:
            self.__voltage = not self.__voltage
        finally:
            self.__lock.release()

    # Мигаем светодиодом: зажигаем его на время secs. Потом если возвращаем к первоначальному состоянию
    def blink(self, secs):
        self.__lock.acquire()
        try:
            if self.__voltage == 0:
                self.__voltage = 1
            else:
                return
        finally:
            self.__lock.release()
        time.sleep(secs)
        self.inverse()


def outForDebug(boolean):
    if boolean:
        print(1, end=' ')
    else:
        print(0, end=' ')


def debugShow(debugPorts):
    if len(debugPorts) != 12:
        print('Чето тут не так переделывай')
        exit(4)
    for i in range(0, 7):
        for j in range(0, 7):
            if i == 0 and j == 3:
                outForDebug(debugPorts[0].isLightOn())
            elif i == 1 and j == 4:
                outForDebug(debugPorts[1].isLightOn())
            elif i == 2 and j == 5:
                outForDebug(debugPorts[2].isLightOn())
            elif i == 3 and j == 6:
                outForDebug(debugPorts[3].isLightOn())
            elif i == 4 and j == 5:
                outForDebug(debugPorts[4].isLightOn())
            elif i == 5 and j == 4:
                outForDebug(debugPorts[5].isLightOn())
            elif i == 6 and j == 3:
                outForDebug(debugPorts[6].isLightOn())
            elif i == 5 and j == 2:
                outForDebug(debugPorts[7].isLightOn())
            elif i == 4 and j == 1:
                outForDebug(debugPorts[8].isLightOn())
            elif i == 3 and j == 0:
                outForDebug(debugPorts[9].isLightOn())
            elif i == 2 and j == 1:
                outForDebug(debugPorts[10].isLightOn())
            elif i == 1 and j == 2:
                outForDebug(debugPorts[11].isLightOn())
            else:
                print(' ', end=' ')
        print()


def timer(ports, start_minutes, start_seconds):
    if type(start_minutes) != int or type(start_seconds) != int:
        print("НЕКОРРЕКТНОЕ ЧИСЛО")
        return
    if start_minutes < 0 or start_minutes > 59:
        print("НЕКОРРЕКТНОЕ КОЛИЧЕСТВО МИНУТ")
        return
    if start_seconds < 0 or start_seconds > 59:
        print("НЕКОРРЕКТНОЕ КОЛИЧЕСТВО СЕКУНД")
        return
    equals = False
    sec_delta = start_seconds - (start_seconds // 5) * 5
    minutes_port = start_minutes
    sec_port = start_seconds // 5 + 1
    while minutes_port >= 0:  # Цикл по всему времени
        if minutes_port != 0:
            ports[minutes_port].lightOn()
        while sec_port >= 0:  # Цикл по секундам в рамках одной минуты
            if sec_port == minutes_port and minutes_port != 0:
                ports[minutes_port].lightOff()
                equals = True
            sec = 0
            sec_delta = 5
            while sec < sec_delta:  # Цикл по 5 секундам (мигание одной лампочки)
                ports[sec_port].lightOn()
                debugShow(ports)
                time.sleep(0.3)
                ports[sec_port].lightOff()
                time.sleep(0.7)
                sec = sec + 1
            sec_port = sec_port - 1

            if equals:
                ports[minutes_port].lightOn()
                equals = False
        sec_port = 11
        if minutes_port != 0:
            ports[minutes_port].lightOff()
        minutes_port = minutes_port - 1
    print("КОНЕЦ")
    # Вызов звукового сигнала TODO


def secundomer():
    ports = []
    sec = 0
    for i in range(0, 12):
        ports.append(IoPort(ioPorts[i]))
    if len(ports) != 12:
        print("ПОРТОВ МНОГО ИЛИ МАЛО РАЗБЕРИСЬ\n (12)")
        exit(3)

    timer(ports, 1, 3)

    while True:
        for i in range(0, 12):
            for j in range(0, 5):
                ports[i].lightOn()
                debugShow(ports)
                print(sec)
                time.sleep(1)
                sec += 1
                ports[i].lightOff()
                debugShow(ports)


#   Устанавливает будильник. alarm_time -
#   либо строка формата "день час:минута", например "17 23:12".
#   либо если очень повезёт datetime
#   перегрузка функции на этом недоязыке, видимо, выглядит так
def setUpAlarm(ports, alarm_time_raw):
    if isinstance(alarm_time_raw, str):
        alarm_time_parsed = datetime.datetime.strptime(alarm_time_raw, '%d %H:%M')
        # Передаём только день и время, остальные параметры берём из текущего времени
        alarm_time = datetime.datetime.now().replace(day=alarm_time_parsed.day, hour=alarm_time_parsed.hour,
                                                     minute=alarm_time_parsed.minute)
    else:
        alarm_time = alarm_time_raw
    delay = alarm_time - datetime.datetime.now()
    if delay.total_seconds() < 0:
        print(f"Будильник: неправильно передано время {alarm_time_parsed}")
        return
    threading.Timer(delay.total_seconds(), lambda: alarm(ports)).start()
    print(f"Будильник: успешно установлен на время {alarm_time}. Зазвонит через {delay.total_seconds()} сек")


def alarm(ports):
    blink_interval = 0.3
    delay_next = 0.1
    circle_count = 30
    for flick in range(circle_count):
        for port in ports:
            threading.Thread(target=port.blink, args=[blink_interval]).start()
            time.sleep(delay_next)


def debugInRealTime(ports):
    while True:
        debugShow(ports)
        time.sleep(0.1)


def main():
    # secundomer()
    check()
    # IO.setmode(IO.BOARD)
    ports = []

    for i in range(0, 12):
        ports.append(IoPort(ioPorts[i]))
    if len(ports) != 12:
        print("ПОРТОВ МНОГО ИЛИ МАЛО РАЗБЕРИСЬ\n (12)")
        exit(3)

    debugShow(ports)

    # Будильник
    alarm_delay_in_secs = 10
    alarm_time = datetime.datetime.now()
    alarm_time += datetime.timedelta(seconds=alarm_delay_in_secs)
    setUpAlarm(ports, alarm_time)
    # threading.Timer(10, debugInRealTime, args=[ports]).start() #Раскомментить чтобы видеть статус циферблата в реалтайме

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t", ["time="])
    except:
        print("Неправильно параметры передал, лох!")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-t", "--time"):
            setUpAlarm(ports, arg)

    return 0


if __name__ == '__main__':
    main()
