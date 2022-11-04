# import RPi.GPIO as IO
import threading

from components.IoPort import IoPort
from components.alarm import setUpAlarm
from config import ioPorts, groundPorts, uselessPorts, allPorts
from hand_detect import run_until_hand_detected
from utils import check, debugShow, debugInRealTime

INFO = "Программа часы:\n" \
       "help - вывести информацию о функциях программы\n" \
       "exit - завершить программу\n" \
       "alarm day hour:minute - поставить будильник на соответствующее время\n" \
       "Например 21 08:20 -> будильник поставлен на 21 число время 8 часов 20 минут\n" \
       "secundomer -\n" \
       "timer - \n" \
       "clock - \n"  # TODO  дописать доку для своих функций


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
        # IO.setup(self.__ioPort, IO.OUT)
        # IO.output(self.__ioPort, self.__voltage)

    def get(self):
        if not (self.__ioPort in inUsePorts):
            print("ПОРТ НЕПРАВИЛЬНО УКАЗАН ВСЁ СГОРИТ (Get)\n")
            exit(2)
        return self.__ioPort

    def lightOn(self):
        if self.__voltage == 1:
            print('Порт ', self.__ioPort, ' два раза зажгли одно и то же!!!\n')
            exit(3)
        self.__voltage = 1
        print('Порт номер ', self.__ioPort, ' светится\n')
        # IO.output(self.__ioPort, self.__voltage)

    def lightOff(self):
        if self.__voltage == 0:
            print('Два раза выключили одно и то же!!!\n')
            exit(3)
        self.__voltage = 0
        print('Порт номер ', self.__ioPort, ' мрак\n')
        # IO.output(self.__ioPort, 0)

    def isLightOn(self):
        return self.__voltage == 1


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

        
def endTIme(ports):
    ports[0].lightOn()
    for i in range(1, 12):
        debugShow(ports)
        time.sleep(0.1)
        ports[i].lightOn()
        debugShow(ports)
        time.sleep(0.1)
        ports[i-1].lightOff()
    ports[11].lightOff()
    debugShow(ports)


def timer(ports, start_minutes, start_seconds):
    if type(start_minutes) != int or type(start_seconds) != int:
        print("НЕКОРРЕКТНОЕ ЧИСЛО")
        return
    if start_minutes < 0 or start_minutes > 11:
        print("НЕКОРРЕКТНОЕ КОЛИЧЕСТВО МИНУТ")
        return
    if start_seconds < 0 or start_seconds > 59:
        print("НЕКОРРЕКТНОЕ КОЛИЧЕСТВО СЕКУНД")
        return
    is_first_iteration = True
    is_equals = False
    minutes_port = start_minutes
    sec_port = start_seconds // 5
    while minutes_port >= 0:  # Цикл по всему времени
        if minutes_port != 0:
            ports[minutes_port].lightOn()
        while sec_port >= 0:  # Цикл по секундам в рамках одной минуты
            sec = 0
            sec_delta = 5
            if is_first_iteration:
                sec_delta = start_seconds - (start_seconds // 5) * 5
                is_first_iteration = False

            if sec_port == minutes_port and minutes_port != 0:
                num_iter = 0
                while sec < sec_delta:  # Цикл по 5 секундам (мигание одной лампочки), когда минуты совпали с секундами
                    if num_iter != 0:
                        ports[sec_port].lightOn()
                    num_iter = num_iter + 1
                    is_equals = True
                    debugShow(ports)
                    time.sleep(0.3)
                    ports[sec_port].lightOff()
                    time.sleep(0.7)
                    sec = sec + 1
            else:
                while sec < sec_delta:  # Цикл по 5 секундам (мигание одной лампочки)
                    ports[sec_port].lightOn()
                    debugShow(ports)
                    time.sleep(0.3)
                    ports[sec_port].lightOff()
                    time.sleep(0.7)
                    sec = sec + 1
            sec_port = sec_port - 1
            if is_equals:
                ports[minutes_port].lightOn()
                is_equals = False
        sec_port = 11
        if minutes_port != 0:
            ports[minutes_port].lightOff()
        minutes_port = minutes_port - 1
    print("КОНЕЦ")
    # Вызов звукового сигнала TODO


def secundomer(ports, timetostop):
    sec = 0
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
                if sec == timetostop:
                    return


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


def alarm(ports):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t", ["time="])
    except:
        print("Неправильно параметры передал, лох!")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-t", "--time"):
            setUpAlarm(ports, arg)



def main():
    # secundomer.py()
    check(allPorts, ioPorts, groundPorts, uselessPorts)
    # IO.setmode(IO.BOARD)
    ports = []

    for i in range(0, 12):
        ports.append(IoPort(ioPorts[i]))
    if len(ports) != 12:
        print("ПОРТОВ МНОГО ИЛИ МАЛО РАЗБЕРИСЬ\n (12)")
        exit(3)


    # debugShow(ports)

    # cl = Clock(ports)

    endTIme(ports)



    print(INFO)


    #threading.Thread(target=debugInRealTime, args=[ports]).start() # FIXME Раскомментить чтобы видеть статус циферблата в реалтайме
    while True:
        raw_input = input()  # читаем команды в формате "команда аргументы"
        parse_input = raw_input.partition(' ')
        func = parse_input[0]
        args = parse_input[2]
        if func not in {"help", "exit", "secundomer", "alarm", "timer"}:
            print("Неправильные аргументы")
            print(INFO)
            continue
        if func == "help":
            print(INFO)
        if func == "exit":
            exit(0)
        if func == "alarm":
            setUpAlarm(ports, args) #FIXME пример вызовы своей функции
        # TODO дописываем свои функции
        
    return 0


if __name__ == '__main__':
    main()
