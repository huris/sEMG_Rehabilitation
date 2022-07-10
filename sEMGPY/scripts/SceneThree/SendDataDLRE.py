import multiprocessing
import numpy as np
import socket
import torch
from tsai.inference import load_learner
import joblib
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import warnings
warnings.filterwarnings(action="ignore")

from pyomyo import Myo, emg_mode


# %% 机器学习模型
# 加载机器学习模型
MLModels = joblib.load('models/sEMGML.pkl')
# 初始化最优权重值
MLWeight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])

# %% 深度学习模型
# 加载深度学习回归模型
DLModels = {}
DLModels['10LSTM'] = load_learner('models/10LSTMRegression.pkl', cpu=False)
DLModels['11LSTM'] = load_learner('models/11LSTMRegression.pkl', cpu=False)
# DLModels['12LSTM'] = load_learner('models/12LSTMRegression.pkl', cpu=False)
# DLModels['13LSTM'] = load_learner('models/13LSTMRegression.pkl', cpu=False)
DLModels['14LSTM'] = load_learner('models/14LSTMRegression.pkl', cpu=False)
DLModels['15XCMPlus'] = load_learner('models/15XCMPlusRegression.pkl', cpu=False)
# 初始化最优权重值
DLWeight = np.array([0.45, 0.26, 0.14, 0.15])

# %% 训练
window_size = 23  # 滑动窗口大小为7
half_window_size = window_size // 2
window_weight = torch.tensor([1 / window_size for i in range(0, window_size)])
MLDL_weight = torch.tensor([0.0692, 0.9308])

idx = 0
window_slide = torch.zeros(window_weight.shape)
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

        # 八个通道的sEMG值, 角的运动值, 时间
        # data = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time"]

        while True:

            # sEMG = q.get()   # 8个通道的sEMG信号
            # # 做一些处理
            # sEMG = np.array([84, 268, 736, 161, 57, 285, 76, 209]).reshape(1, -1)

            sEMG = np.array(q.get()).reshape(1, -1)
            sEMG = sEMG.astype(np.float32)

            # ML
            MLResults = 0
            for i, j in enumerate(MLModels):
                MLResults += MLWeight[i] * MLModels[j].predict(sEMG)

            # DL
            DLResults = 0
            for i, j in enumerate(DLModels):
                sEMG = sEMG.reshape(1, 1, 8)
                _, _, preds = DLModels[j].get_X_preds(sEMG)
                DLResults += DLWeight[i] * np.array(preds)

            sEMG = MLDL_weight[0] * MLResults + MLDL_weight[1] * DLResults

            # 先把数据填满
            if isWindowsEmpty:
                window_slide[idx] = sEMG
                idx += 1

                if idx == window_size:
                    idx = half_window_size
                    isWindowsEmpty = False
                else:
                    continue

            # 投票算法
            window_slide[(idx + half_window_size) % window_size] = sEMG

            window_slide[idx] *= window_weight[0]

            for i in range(1, window_size, 1):
                window_slide[idx] += window_slide[(idx + i) % window_size] * window_weight[i]

            # 发送过去
            client_executor.send(bytes(repr(round(window_slide[idx].item(), 2)).encode('utf-8')))
            msg = client_executor.recv(1024).decode('utf-8')

            # unity退出发出信号‘2’
            if msg == '2':
                break

            if idx < window_size - 1:
                idx += 1
            else:
                idx = 0

        client_executor.close()
        print('断开连接: %s:%s' % addr)

        p.terminate()
        p.join()