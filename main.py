# import RPi.GPIO as IO
import threading

from components.IoPort import IoPort
from components.alarm import setUpAlarm
from config import ioPorts, groundPorts, uselessPorts
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

    debugShow(ports)

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
