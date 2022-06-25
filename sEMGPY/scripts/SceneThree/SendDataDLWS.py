import multiprocessing
import numpy as np
import socket
import time
import datetime
import warnings
warnings.filterwarnings(action="ignore")

from pyomyo import Myo, emg_mode

from tsai.inference import load_learner

import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import warnings
warnings.filterwarnings(action="ignore")

# 加载深度学习模型
DLModels = {}
DLModels['30LSTM'] = load_learner('models/30LSTMRegression.pkl', cpu=False)
DLModels['31LSTM'] = load_learner('models/31LSTMRegression.pkl', cpu=False)
DLModels['32LSTM'] = load_learner('models/32LSTMRegression.pkl', cpu=False)
DLModels['33MLSTM_FCN'] = load_learner('models/33MLSTM_FCNRegression.pkl', cpu=False)

# 初始化最优权重值
DLWeight = np.array([0.15, 0.25, 0.28, 0.32], dtype=np.float)

# 滑动窗口矫正
DL_Corr = 1.1338749861340824

# 训练
window_size = 23  # 滑动窗口大小为7
half_window_size = window_size // 2
window_weight = np.array([1 / window_size for i in range(0, window_size)])

idx = 0
window_slide = np.zeros(window_weight.shape)
isWindowsEmpty = True

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

    # 进入死循环,等待新的客户端连入
    while True:
        client_executor, addr = listener.accept()
        print('监听连接: %s:%s...' % addr)

        # 连接成功后, 先清空之前的缓存
        while not q.empty():
            q.get()

        start_time = time.time()
        start_time_ns = time.perf_counter_ns()

        # 八个通道的sEMG值, 角的运动值, 时间
        # data = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time"]
        data = []

        while True:

            # sEMG = q.get()   # 8个通道的sEMG信号
            # # 做一些处理
            # sEMG = np.array([84, 268, 736, 161, 57, 285, 76, 209]).reshape(1, -1)

            d = list(q.get())

            sEMG = np.array(d, dtype=np.float).reshape(1, 1, 8)

            DLResults = 0
            for i, j in enumerate(DLModels):
                _, _, preds = DLModels[j].get_X_preds(sEMG)
                DLResults += DLWeight[i] * np.array(preds)

            if DLResults > 1:
                DLResults = 1
            elif DLResults < 0:
                DLResults = 0

            # 先把数据填满
            if isWindowsEmpty:
                window_slide[idx] = DLResults
                idx += 1

                if idx == window_size:
                    idx = half_window_size
                    isWindowsEmpty = False
                else:
                    continue

            # 投票算法
            window_slide[(idx + half_window_size) % window_size] = DLResults

            window_slide[idx] *= window_weight[0]

            for i in range(1, window_size, 1):
                window_slide[idx] += window_slide[(idx + i) % window_size] * window_weight[i]

            # 发送过去
            value = round((window_slide[idx].item() - 0.5) * DL_Corr + 0.5 , 2)
            client_executor.send(bytes(repr(value).encode('utf-8')))
            msg = client_executor.recv(1024).decode('utf-8')

            d.append(value)
            d.append(time.perf_counter_ns() - start_time_ns)
            data.append(d)

            # unity退出发出信号‘2’
            if msg == '2':
                break

            if idx < window_size - 1:
                idx += 1
            else:
                idx = 0

        client_executor.close()
        print('断开连接: %s:%s' % addr)

        # 保存数据
        np_data = np.asarray(data)
        np.savetxt("./experiment/" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".csv", np_data, delimiter=",")
        print("数据已保存")

        p.terminate()
        p.join()