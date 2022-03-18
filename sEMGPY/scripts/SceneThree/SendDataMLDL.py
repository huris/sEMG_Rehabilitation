# Preprocessing tools
import math
import time
import numpy as np
import pandas as pd

# DL/ML Algoirthm
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from tsai.all import *
from tsai.inference import load_learner

import joblib
import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import warnings
warnings.filterwarnings(action="ignore")


# 不打印
sys.stdout = open(os.devnull, 'w')
# 打印
# sys.stdout = sys.__stdout__


cols = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time_ns"]

train1_data = pd.read_csv("data/Train1.csv", header=None)
train2_data = pd.read_csv("data/Train2.csv", header=None)
train3_data = pd.read_csv("data/Train3.csv", header=None)
train_data = pd.read_csv("data/Train.csv", header=None)

test_data = pd.read_csv("data/Test.csv", header=None)
valid_data = pd.read_csv("data/Valid.csv", header=None)

train_data.columns = test_data.columns = valid_data.columns = cols

train_features = train_data.drop(['Rect', 'Time_ns'], axis=1)
train_labels = train_data.Rect
train_all = pd.concat([train_features, train_labels], axis=1, ignore_index=True, sort=False)
train_six_features = train_data.drop(['Two', 'Five', 'Rect', 'Time_ns'], axis=1)
train_two_features = pd.concat([train_data.Three, train_data.Four], axis=1, ignore_index=False, sort=False)

test_features = test_data.drop(['Rect', 'Time_ns'], axis=1)
test_labels = test_data.Rect
test_all = pd.concat([test_features, test_labels], axis=1, ignore_index=True, sort=False)
test_six_features = test_data.drop(['Two', 'Five', 'Rect', 'Time_ns'], axis=1)
test_two_features = pd.concat([test_data.Three, test_data.Four], axis=1, ignore_index=False, sort=False)

valid_features = valid_data.drop(['Rect', 'Time_ns'], axis=1)
valid_labels = valid_data.Rect
valid_all = pd.concat([valid_features, valid_labels], axis=1, ignore_index=True, sort=False)
valid_six_features = valid_data.drop(['Two', 'Five', 'Rect', 'Time_ns'], axis=1)
valid_two_features = pd.concat([valid_data.Three, valid_data.Four], axis=1, ignore_index=False, sort=False)

sEMG_all = pd.concat([train_all, test_all], axis=0, ignore_index=True, sort=False)

train_all.columns = test_all.columns = valid_all.columns = sEMG_all.columns = cols[:-1]
# train_features, train_labels, train_all, sEMG_all, train_six_features, train_two_features


# ML
# 加载机器学习模型
MLModels = joblib.load('models/sEMGML.pkl')
# 初始化最优权重值
MLWeight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])


# DL
# 加载深度学习回归模型
DLModels = {}
DLModels['10LSTM'] = load_learner(Path('./models/10LSTMRegression.pkl'), cpu=False)
DLModels['11LSTM'] = load_learner(Path('./models/11LSTMRegression.pkl'), cpu=False)
DLModels['12LSTM'] = load_learner(Path('./models/12LSTMRegression.pkl'), cpu=False)
DLModels['13LSTM'] = load_learner(Path('./models/13LSTMRegression.pkl'), cpu=False)
DLModels['14LSTM'] = load_learner(Path('./models/14LSTMRegression.pkl'), cpu=False)
DLModels['15XCMPlus'] = load_learner(Path('./models/15XCMPlusRegression.pkl'), cpu=False)
# 初始化最优权重值
DLWeight = np.array([0.45, 0.26, 0, 0, 0.14, 0.15])

for index, row in valid_features.iterrows():
    sEMG = np.array(row).reshape(1, -1)

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
    print(MLResults, DLResults)
    break



















# import multiprocessing
# import numpy as np
# import time
# import datetime
# import socket
# import joblib
# import warnings
#
# warnings.filterwarnings(action="ignore")
#
# from pyomyo import Myo, emg_mode
#
# # 加载集成学习模型
# models = joblib.load('models/sEMGML.pkl')
# # 初始化最优权重值
# best_weight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])
#
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
#             # sEMG = q.get()   # 8个通道的sEMG信号
#             # # 做一些处理
#             # sEMG = np.array([84, 268, 736, 161, 57, 285, 76, 209]).reshape(1, -1)
#             # # [0.43085063, 0.30477173, 0.22223776, 0.22317647, 0.28845479, 0.37974083]
#
#             sEMG = np.array(q.get()).reshape(1, -1)
#
#             # 集成学习: SVR, LGB, RF, GBRT, XGB, Bagging
#             re = 0
#             for i, j in enumerate(models):
#                 re += best_weight[i] * models[j].predict(sEMG)
#
#             # 发送过去
#             client_executor.send(bytes(repr(round(re[0], 2)).encode('utf-8')))
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
