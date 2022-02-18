import pygame
import multiprocessing
from pyomyo import Myo, emg_mode

# ------------ Myo手环设置 ---------------
q = multiprocessing.Queue()
emgColor =[[ 25, 202, 173],
           [190, 231, 233],
           [214, 213, 183],
           [209, 186, 116],
           [230, 206, 172],
           [236, 173, 158],
           [244,  96, 108],
           [140, 199, 181]]


def worker(q):
    m = Myo(mode=emg_mode.PREPROCESSED)
    m.connect()

    def add_to_queue(emg, movement):
        q.put(emg)

    m.add_emg_handler(add_to_queue)

    def print_battery(bat):
        print("Battery level:", bat)

    m.add_battery_handler(print_battery)

    # 改变Myo的led颜色灯, 展示数据为红色
    m.set_leds([128, 0, 0], [128, 0, 0])
    # 连接成功颤动一下
    m.vibrate(1)

    """worker function"""
    while True:
        m.run()
    print("Worker Stopped")


last_vals = None


def plot(scr, vals):
    DRAW_LINES = True

    global last_vals
    if last_vals is None:
        last_vals = vals
        return

    D = 5
    scr.scroll(-D)
    scr.fill((0, 0, 0), (w - D, 0, w, h))
    for i, (u, v) in enumerate(zip(last_vals, vals)):
        if DRAW_LINES:
            pygame.draw.line(scr, emgColor[i],
                             (w - D, int(h / 9 * (i + 1 - u))),
                             (w, int(h / 9 * (i + 1 - v))))
            pygame.draw.line(scr, (255, 255, 255),
                             (w - D, int(h / 9 * (i + 1))),
                             (w, int(h / 9 * (i + 1))))
        else:
            c = int(255 * max(0, min(1, v)))
            scr.fill((c, c, c), (w - D, i * h / 8, D, (i + 1) * h / 8 - i * h / 8))

    pygame.display.flip()
    last_vals = vals


if __name__ == "__main__":
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()

    w, h = 800, 600
    scr = pygame.display.set_mode((w, h))

    try:
        while True:
            # 处理pygame事件以保持窗口响应
            pygame.event.pump()
            # 获取emg信号并绘制
            while not (q.empty()):
                emg = list(q.get())
                plot(scr, [e / 500. for e in emg])
                print(emg)

    except KeyboardInterrupt:
        print("Quitting")
        pygame.quit()
        quit()