import multiprocessing
import numpy as np
import time
import datetime
import socket
import joblib

from pyomyo import Myo, emg_mode

# 加载集成学习模型
models = joblib.load('models/sEMGML.pkl')
# 初始化最优权重值
best_weight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])

sEMG = np.array([84, 268, 736, 161, 57, 285, 76, 209])
# [0.43085063, 0.30477173, 0.22223776, 0.22317647, 0.28845479, 0.37974083]
anglePercent = np.array()



# q = multiprocessing.Queue()
#
#
# def worker(q, MODE):
#     m = Myo(mode=MODE)
#     m.connect()
#
#     def add_to_queue(emg, movement):
#         q.put(emg)
#
#     m.add_emg_handler(add_to_queue)
#
#     # 训练时设置为橘色
#     m.set_leds([128, 128, 0], [128, 128, 0])
#     # 当手环连接成功时颤动一下
#     m.vibrate(1)
#
#     while True:
#         m.run()
#
#
# if __name__ == "__main__":
#
#     MODE = emg_mode.PREPROCESSED
#     p = multiprocessing.Process(target=worker, args=(q, MODE))
#     p.start()
#
#     # 构建Socket实例,设置端口号和监听队列大小
#     listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     listener.bind(('127.0.0.1', 10086))
#     listener.listen(5)
#
#     # 进入死循环,等待新的客户端连入
#     while True:
#         client_executor, addr = listener.accept()
#         print('监听连接: %s:%s...' % addr)
#
#         # 连接成功后, 先清空之前的缓存
#         while not q.empty():
#             q.get()
#
#         # 八个通道的sEMG值, 角的运动值, 时间
#         # data = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time"]
#
#         while True:
#
            # sEMG = q.get()   # 8个通道的sEMG信号
#             # 做一些处理
#
#             # 发送过去
#             client_executor.send(bytes(repr(round(sEMG[3] / 500, 2)).encode('utf-8')))
#             msg = client_executor.recv(1024).decode('utf-8')
#
#             # unity退出发出信号‘2’
#             if msg == '2':
#                 break
#
#         client_executor.close()
#         print('断开连接: %s:%s' % addr)
#
#         p.terminate()
#         p.join()