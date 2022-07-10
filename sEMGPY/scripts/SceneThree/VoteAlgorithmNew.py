import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas_profiling as ppf

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

# import data
import joblib

import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import warnings
warnings.filterwarnings(action="ignore")

def R2Score(YTrue, YPre):
    u = ((YTrue - YPre) ** 2).sum()
    v = ((YTrue - YTrue.mean()) ** 2).sum()
    return 1 - u / v

# %% 导入数据
cols = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Rect", "Time_ns"]
PATH = "scripts/SceneThree/"

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
train_features, train_labels, train_all, sEMG_all, train_six_features, train_two_features

# %% 机器学习模型
# 加载机器学习模型
MLModels = joblib.load(PATH + 'models/sEMGML.pkl')

# 初始化最优权重值
MLWeight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])

# %% ML测试
MLTrain_Results = np.zeros((train_features.shape[0], len(MLModels)))
MLTest_Results = np.zeros((test_features.shape[0], len(MLModels)))
MLValid_Results = np.zeros((valid_features.shape[0], len(MLModels)))


idx = 0

start = time.perf_counter()

for model in MLModels:
    MLTrain_Results[:, idx] = MLModels[model].predict(train_features)
    MLTest_Results[:, idx] = MLModels[model].predict(test_features)
    MLValid_Results[:, idx] = MLModels[model].predict(valid_features)
    idx += 1

end = time.perf_counter()
print("time consuming : {:.4f}ms".format((end - start) * 1000))

MLTrain_Results, MLTest_Results, MLValid_Results

# %%
R2Score(train_labels, MLTrain_Results @ MLWeight)

# %%
R2Score(test_labels, MLTest_Results @ MLWeight)

# %%
R2Score(valid_labels, MLValid_Results @ MLWeight)

# %% 深度学习模型
DLTrain_Features = torch.tensor(train_data.drop(['Rect', 'Time_ns'], axis=1).values, dtype=torch.float32).reshape(-1, 1, 8)
DLTrain_Labels = torch.tensor(train_data.Rect.values.reshape(-1, 1), dtype=torch.float32).reshape(-1)

DLTest_Features = torch.tensor(test_data.drop(['Rect', 'Time_ns'], axis=1).values, dtype=torch.float32).reshape(-1, 1, 8)
DLTest_Labels = torch.tensor(test_data.Rect.values.reshape(-1, 1), dtype=torch.float32).reshape(-1)

DLValid_Features = torch.tensor(valid_data.drop(['Rect', 'Time_ns'], axis=1).values, dtype=torch.float32).reshape(-1, 1, 8)
DLValid_Labels = torch.tensor(valid_data.Rect.values.reshape(-1, 1), dtype=torch.float32).reshape(-1)

# %% 加载深度学习回归模型
DLModels = {}
DLModels['30LSTM'] = load_learner(Path(PATH + 'models/30LSTMRegression.pkl'), cpu=False)
DLModels['31LSTM'] = load_learner(Path(PATH + 'models/31LSTMRegression.pkl'), cpu=False)
DLModels['32LSTM'] = load_learner(Path(PATH + 'models/32LSTMRegression.pkl'), cpu=False)
DLModels['33MLSTM_FCN'] = load_learner(Path(PATH + 'models/33MLSTM_FCNRegression.pkl'), cpu=False)

# 初始化最优权重值
DLWeight =  torch.tensor([0.15, 0.25, 0.28, 0.32], dtype=torch.float32)

# %% 深度学习测试
DLTrainProbas = {}
DLTestProbas = {}
DLValidProbas = {}

start = time.perf_counter()
for i in DLModels:
    DLTrainProbas[i], _, _ = DLModels[i].get_X_preds(DLTrain_Features)
    DLTestProbas[i], _, _ = DLModels[i].get_X_preds(DLTest_Features)
    DLValidProbas[i], _, _ = DLModels[i].get_X_preds(DLValid_Features)

end = time.perf_counter()
print("time consuming : {:.4f}ms".format((end - start) * 1000))

# %%
DLTrainProbasCat = torch.cat([DLTrainProbas[i] for i in DLTrainProbas], 1)
DLTestProbasCat = torch.cat([DLTestProbas[i] for i in DLTestProbas], 1)
DLValidProbasCat = torch.cat([DLValidProbas[i] for i in DLValidProbas], 1)

# %%
for i in range(0, 4):
    print(R2Score(DLTrain_Labels, DLTrainProbasCat[:,i]))

R2Score(DLTrain_Labels, DLTrainProbasCat @ DLWeight)

# %%
for i in range(0, 4):
    print(R2Score(DLTest_Labels, DLTestProbasCat[:,i]))

R2Score(DLTest_Labels, DLTestProbasCat @ DLWeight)

# %%
for i in range(0, 4):
    print(R2Score(DLValid_Labels, DLValidProbasCat[:,i]))

R2Score(DLValid_Labels, DLValidProbasCat @ DLWeight)

# %%
MLDL_weight = np.array([0.2112, 0.7888])

# start = time.perf_counter()
MLDLTrainResult = np.array((MLTrain_Results @ MLWeight, np.array(DLTrainProbasCat @ DLWeight))).T @ MLDL_weight
MLDLTestResult = np.array((MLTest_Results @ MLWeight, np.array(DLTestProbasCat @ DLWeight))).T @ MLDL_weight
MLDLValidResult = np.array((MLValid_Results @ MLWeight, np.array(DLValidProbasCat @ DLWeight))).T @ MLDL_weight
# end = time.perf_counter()
# print("time consuming : {:.4f}ms".format((end - start) * 1000))
print(R2Score(train_labels, MLDLTrainResult))
print(R2Score(test_labels, MLDLTestResult))
print(R2Score(valid_labels, MLDLValidResult))


# %%
results = np.array((100, 1))

ResultsIterrows = MLDLTestResult

raw_labels = test_labels

ML_Corr = 1.1169662217712004
DL_Corr = 1.1338749861340824
MLDL_Corr = 1.1273286680299455
#
Corr = MLDL_Corr

for ii in range(21, 22, 2):
    start = time.perf_counter()

    window_size = ii  # 滑动窗口大小
    half_window_size = window_size // 2
    window_weight = np.array([1 / ii for i in range(0, ii)])
    # window_weight = np.array([0.8, 0.05, 0.03, 0.02, 0.02, 0.03, 0.05])

    idx = 0
    window_slide = np.zeros(window_weight.shape)
    re = np.zeros(raw_labels.shape)
    re_idx = 0

    isWindowsEmpty = True

    for sEMG in ResultsIterrows:
        # 先把数据填满
        if isWindowsEmpty:
            window_slide[idx] = sEMG
            # 保存结果
            if idx < half_window_size:
                re[re_idx] = sEMG
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

        if re_idx == raw_labels.shape[0] - half_window_size:
            while re_idx < raw_labels.shape[0]:
                idx = (idx + 1) % window_size
                re[re_idx] = window_slide[idx].item()
                re_idx += 1

        if idx < window_size - 1:
            idx += 1
        else:
            idx = 0

    re = (re - 0.5) * Corr + 0.5  # 修正结果

    print(ii)
    # results[ii] = R2Score(raw_labels, re)  # 循环i
    results = R2Score(raw_labels, re)  # 单个i

    end = time.perf_counter()
    # print("time consuming : {:.4f}ms".format((end - start) * 1000))

    # print(ii, results[ii])  # 循环i
    print(ii, results)  # 单个i

# %%
plt.figure()
plt.plot(np.arange(len(raw_labels)), raw_labels,'go-',label='True Value')
plt.plot(np.arange(len(raw_labels)), re, 'ro-',label='Predict Value')
# plt.title(f'{name} score: {score}')
plt.xlabel = "Samples"
plt.ylabel = "Angle of Rotation"
plt.legend()
plt.show()






