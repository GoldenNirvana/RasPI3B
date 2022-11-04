from datetime import time

from utils import debugShow


def secundomer(ports):
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

                # тут можно написать число секунд, до скольки будет секундомер считать
                # или можно просто стереть, тогда будет бесконечнл считать
                if sec == 30:
                    return
