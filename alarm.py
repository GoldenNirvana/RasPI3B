import threading
import time
from datetime import datetime


def setUpAlarm(ports, alarm_time_str):
    alarm_time_parsed = datetime.strptime(alarm_time_str, '%d %H:%M')
    # Передаём только день и время, остальные параметры берём из текущего времени
    alarm_time = datetime.now().replace(day=alarm_time_parsed.day, hour=alarm_time_parsed.hour, minute=alarm_time_parsed.minute)
    delay = alarm_time - datetime.now()
    if delay.total_seconds() < 0:
        print(f"Будильник: неправильно передано время {alarm_time_parsed}")
        return
    threading.Timer(delay.total_seconds(), lambda: alarm(ports)).start()
    print(f"Будильник: успешно установлен на время {alarm_time}. Зазвонит через {delay.total_seconds()} сек")


def alarm(ports):
    for flick in range(15):
        for port in ports:
            port.lightOff() if port.isLightOn() else port.lightOn()
        time.sleep(0.3)
