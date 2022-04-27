import numpy as np
import pandas as pd

import joblib

import os
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

# %% 机器学习模型
# 加载机器学习模型
MLModels = joblib.load(PATH + 'models/sEMGML.pkl')
# 初始化最优权重值
MLWeight = np.array([0.42, 0.04, 0.14, 0.11, 0.09, 0.2])


# %%
def R2Score(YTrue, YPre):
    u = ((YTrue - YPre) ** 2).sum()
    v = ((YTrue - YTrue.mean()) ** 2).sum()
    return 1 - u / v

# %% 训练
results = np.zeros((100, 1))
for ii in range(3, 100, 2):
    valid_labels = np.array(valid_labels)
    window_size = ii  # 滑动窗口大小为7
    half_window_size = window_size // 2
    window_weight = np.array([1 / ii for i in range(0, ii)])

    idx = 0
    window_slide = np.zeros(window_weight.shape)
    re = np.zeros(valid_labels.shape)
    re_idx = 0

    isWindowsEmpty = True

    t = 10

    for index, row in valid_features.iterrows():
        sEMG = np.array(row).reshape(1, -1)

        # ML
        MLResults = 0
        for i, j in enumerate(MLModels):
            MLResults += MLWeight[i] * MLModels[j].predict(sEMG)

        sEMG = MLResults

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
        if re_idx == valid_features.shape[0] - half_window_size:
            while re_idx < valid_features.shape[0]:
                idx = (idx + 1) % window_size
                re[re_idx] = window_slide[idx].item()
                re_idx += 1

        if idx < window_size - 1:
            idx += 1
        else:
            idx = 0

    results[ii] = R2Score(valid_labels, re)
    print(ii, results[ii])


# %%
R2Score(valid_labels, re)