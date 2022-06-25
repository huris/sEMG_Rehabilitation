import math
import time
import numpy as np
import pandas as pd

# DL/ML Algoirthm
from tsai.all import *

import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import warnings
warnings.filterwarnings(action="ignore")

# %% 导入数据
PATH = "scripts/SceneThree/"
cols = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time_ns"]

train1_data = pd.read_csv(PATH + "data/Train1.csv", header=None)
train2_data = pd.read_csv(PATH + "data/Train2.csv", header=None)
train3_data = pd.read_csv(PATH + "data/Train3.csv", header=None)
train_data = pd.read_csv(PATH + "data/Train.csv", header=None)

test_data = pd.read_csv(PATH + "data/Test.csv", header=None)
valid_data = pd.read_csv(PATH + "data/Valid.csv", header=None)

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

# %% 深度学习模型
from tsai.inference import load_learner
# # 加载深度学习回归模型
DLModels = {}
DLModels['30LSTM'] = load_learner(Path(PATH + 'models/30LSTMRegression.pkl'), cpu=False)
DLModels['31LSTM'] = load_learner(Path(PATH + 'models/31LSTMRegression.pkl'), cpu=False)
DLModels['32LSTM'] = load_learner(Path(PATH + 'models/32LSTMRegression.pkl'), cpu=False)
DLModels['33MLSTM_FCN'] = load_learner(Path(PATH + 'models/33MLSTM_FCNRegression.pkl'), cpu=False)

# 初始化最优权重值
DLWeight = torch.tensor([0.15, 0.25, 0.28, 0.32], dtype=torch.float32)

# %%
def R2Score(YTrue, YPre):
    u = ((YTrue - YPre) ** 2).sum()
    v = ((YTrue - YTrue.mean()) ** 2).sum()
    return 1 - u / v

# %% 训练
results = np.array((100, 1))
test_labels = np.array(test_labels, dtype=np.float)
test_features = test_features

DL_Corr = 1.1338749861340824

for ii in range(23, 24, 2):
    start = time.perf_counter()

    window_size = ii  # 滑动窗口大小
    half_window_size = window_size // 2
    window_weight = np.array([1 / ii for i in range(0, ii)])

    idx = 0
    window_slide = np.zeros(window_weight.shape)
    re = np.zeros(test_labels.shape)
    re_idx = 0

    isWindowsEmpty = True

    for index, row in test_features.iterrows():
        sEMG = np.array(row, dtype=np.float).reshape(1, 1, 8)

        # DL
        DLResults = 0
        for i, j in enumerate(DLModels):
            _, _, preds = DLModels[j].get_X_preds(sEMG)
            DLResults += DLWeight[i] * np.array(preds)

        sEMG = DLResults

        # 先把数据填满
        if isWindowsEmpty:
            window_slide[idx] = sEMG
            # 保存结果
            if idx < half_window_size:
                re[re_idx] = sEMG.item()
                re_idx += 1

                if re_idx == re.shape[0]:
                    break

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

        re[re_idx] = window_slide[idx].item()
        re_idx += 1

        # print(re_idx)
        if re_idx == test_labels.shape[0] - half_window_size:
            while re_idx < test_labels.shape[0]:
                idx = (idx + 1) % window_size
                re[re_idx] = window_slide[idx].item()
                re_idx += 1

        if idx < window_size - 1:
            idx += 1
        else:
            idx = 0

    re = (re - 0.5) * DL_Corr + 0.5  # 修正结果

    # results[ii] = R2Score(test_labels, re)  # 循环i
    results = R2Score(test_labels, re)  # 单个i

    end = time.perf_counter()
    print("time consuming : {:.4f}ms".format((end - start) * 1000))

    # print(ii, results[ii]) # 循环i
    print(ii, results)  # 单个i


# %%
plt.figure()
plt.plot(np.arange(len(test_labels)), test_labels,'go-',label='True Value')
plt.plot(np.arange(len(test_labels)), re, 'ro-',label='Predict Value')
# plt.title(f'{name} score: {score}')
plt.xlabel = "Samples"
plt.ylabel = "Angle of Rotation"
plt.legend()
plt.show()