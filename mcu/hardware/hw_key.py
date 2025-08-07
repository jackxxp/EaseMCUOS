import io
import sys
from machine import Pin, PWM
import _thread

# 版本信息
keyver, keyupdatedate = 1.0, 20250807

class DualButtonWithLED:
    def __init__(self, debug=0):
        self.debug = debug
        try:
            self.lock = _thread.allocate_lock()
            self.main_button = Pin(0, Pin.IN, Pin.PULL_UP)
            self.power_button = Pin(10, Pin.IN, Pin.PULL_UP)
            self.led_pwm = PWM(Pin(9))
            self.led_pwm.freq(1000)
            self.led_pwm.duty_u16(0)
            print(f"<key> 信息 版本:{keyver} 更新日期:{keyupdatedate}")
        except Exception as e:
            print("<key> 错误 初始化错误:")
            print(self._format_exception(e))

    def _format_exception(self, e):
        buf = io.StringIO()
        sys.print_exception(e, buf)
        return buf.getvalue()

    def getmainkey(self):
        try:
            state = not self.main_button.value()
            if self.debug and state:
                print(f"<key> 调试 主按键被按下")
            return state
        except Exception as e:
            print("<key> 错误 主按键读取错误:")
            print(self._format_exception(e))
            return False

    def getpowerkey(self):
        try:
            state = not self.power_button.value()
            if self.debug and state:
                print(f"<key> 调试 电源按键被按下")
            return state
        except Exception as e:
            print("<key> 错误 电源按键读取错误:")
            print(self._format_exception(e))
            return False


    def setled(self, freq=None, duty=None):
        try:
            with self.lock:
                if freq is not None:
                    if isinstance(freq, int) and 5 <= freq <= 10000:
                        self.led_pwm.freq(freq)
                        if self.debug:
                            print(f"<key> 调试 设置频率: {freq}")
                    else:
                        raise ValueError(f"频率参数非法: {freq}")
                if duty is not None:
                    if isinstance(duty, int) and 0 <= duty <= 65535:
                        self.led_pwm.duty_u16(duty)
                        if self.debug:
                            print(f"<key> 调试 设置占空比: {duty}")
                    else:
                        raise ValueError(f"占空比参数非法: {duty}")
        except Exception as e:
            print("<key> 错误 LED 设置错误:")
            print(self._format_exception(e))



    def deinit(self):
        try:
            with self.lock:
                self.led_pwm.deinit()
                if self.debug:
                    print("<key> 调试 LED PWM 已释放")
        except Exception as e:
            print("<key> 错误 LED 释放错误:")
            print(self._format_exception(e))
