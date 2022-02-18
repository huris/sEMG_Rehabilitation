import multiprocessing
import numpy as np
import time
import datetime
import socket

from pyomyo import Myo, emg_mode

q = multiprocessing.Queue()


def worker(q, MODE):
    m = Myo(mode=MODE)
    m.connect()

    def add_to_queue(emg, movement):
        q.put(emg)

    m.add_emg_handler(add_to_queue)

    # 训练时设置为橘色
    m.set_leds([128, 128, 0], [128, 128, 0])
    # 当手环连接成功时颤动一下
    m.vibrate(1)

    while True:
        m.run()


if __name__ == "__main__":

    MODE = emg_mode.PREPROCESSED
    p = multiprocessing.Process(target=worker, args=(q, MODE))
    p.start()

    # 构建Socket实例,设置端口号和监听队列大小
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 10086))
    listener.listen(5)

    # 初始化实验变量
    TIMER = True
    TimeLimit = 60

    # 进入死循环,等待新的客户端连入
    while True:
        client_executor, addr = listener.accept()
        print('监听连接: %s:%s...' % addr)

        while not q.empty():
            q.get()

        start_time = time.time()
        start_time_ns = time.perf_counter_ns()

        # 八个通道的sEMG值, 角的运动值, 时间
        # data = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time"]
        data = []

        while True:
            client_executor.send(bytes(repr("10101011").encode('utf-8')))

            msg = client_executor.recv(1024).decode('utf-8')
            # print(msg)
            while not q.empty():
                d = list(q.get())
                d.append(float(msg))
                d.append(time.perf_counter_ns() - start_time_ns)
                data.append(d)

            # 如果到达时间了,则退出采集
            if TIMER:
                time_elapsed = time.time() - start_time
                if time_elapsed > TimeLimit:
                    break

            # unity退出发出信号‘2’
            if msg == '2':
                break

        client_executor.close()
        print('断开连接: %s:%s' % addr)

        # 保存数据
        np_data = np.asarray(data)
        np.savetxt("./data/" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".csv", np_data, delimiter=",")
        print("数据已保存")

        p.terminate()
        p.join()