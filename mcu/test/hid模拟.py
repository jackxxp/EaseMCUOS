import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
import time

# 1. 创建并注册 HID 接口
kbd = KeyboardInterface()
usb.device.get().init(kbd)

# 2. 等待 USB 枚举完成
time.sleep_ms(1000)

# 3. 打字：H → I → ENTER
for k in (KeyCode.H, KeyCode.I, KeyCode.ENTER):
    kbd.send_keys([k])  # 按下
    kbd.send_keys([])   # 立即释放
    time.sleep_ms(50)