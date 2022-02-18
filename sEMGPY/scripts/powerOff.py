from pyomyo import Myo, emg_mode

# 关闭myo手环, 省电
# 如果想要重新开启, 连接usb到电脑上

m = Myo(mode=emg_mode.RAW)
m.connect()
m.vibrate(1)
m.power_off()
quit()