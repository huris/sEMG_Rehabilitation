import time
import datetime
import multiprocessing
import pandas as pd
from pyomyo import Myo, emg_mode


def data_worker(mode, seconds, filepath):
    collect = True

    # ------------ Myo手环设置 ---------------
    m = Myo(mode=mode)
    m.connect()

    myo_data = []

    def add_to_queue(emg, movement):
        myo_data.append(emg)

    m.add_emg_handler(add_to_queue)

    def print_battery(bat):
        print("Battery level:", bat)

    m.add_battery_handler(print_battery)

    # 改变Myo的led颜色灯, 采集数据为绿色
    m.set_leds([0, 128, 0], [0, 128, 0])
    # 连接成功颤动一下
    m.vibrate(1)

    print(f"开始采集肌电数据, 共计{seconds}秒")
    # 开始采集数据
    start_time = time.time()

    while collect:
        if time.time() - start_time < seconds:
            m.run()
        else:
            collect = False
            collection_time = time.time() - start_time
            print("完成采集")
            print(f"采集总耗时: {collection_time}")
            print("采集总帧数: ", len(myo_data))

            # 表头
            myo_cols = ["Channel_1", "Channel_2", "Channel_3", "Channel_4", "Channel_5", "Channel_6", "Channel_7",
                        "Channel_8"]
            myo_df = pd.DataFrame(myo_data, columns=myo_cols)

            # 保存数据
            myo_df.to_csv(filepath, index=False)


if __name__ == '__main__':
    # 采集秒数
    seconds = 10
    file_name = "./../dataset/" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".csv"
    mode = emg_mode.PREPROCESSED
    p = multiprocessing.Process(target=data_worker, args=(mode, seconds, file_name))
    p.start()
