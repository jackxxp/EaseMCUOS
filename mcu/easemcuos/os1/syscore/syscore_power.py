from machine import ADC, Pin
import time
import _thread

class Battery:
    def __init__(self,
                 adc_pin=2,
                 charge_detect_pin=3,
                 v_full=12.4,
                 v_half=11.5,
                 v_empty=10.2,
                 charge_threshold=12.8,
                 voltage_divider_ratio=5.0):
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

        self.charge_detect = Pin(charge_detect_pin, Pin.IN)

        self.v_full = v_full
        self.v_half = v_half
        self.v_empty = v_empty
        self.charge_threshold = charge_threshold
        self.divider_ratio = voltage_divider_ratio

        # 初始化估算 SOC
        estimated_soc = self.get_soc()
        if estimated_soc is not None:
            self.avg_soc = estimated_soc
            print(f"<syscorepower> 信息 初始估算SOC: {self.avg_soc}%")
        else:
            self.avg_soc = 0
            print("<syscore_power> 警告 初始估算失败，默认SOC为0")

        # 启动后台线程
        _thread.start_new_thread(self._soc_monitor_thread, ())

    def get_voltage(self):
        try:
            raw = self.adc.read()
            voltage_out = raw * 3.3 / 4095
            voltage_in = voltage_out * self.divider_ratio
            return round(voltage_in, 2)
        except Exception as e:
            print(f"[syscore_power] 获取电压失败: {e}")
            return None

    def is_charging(self):
        try:
            return bool(self.charge_detect.value())
        except Exception as e:
            print(f"[syscore_power] 获取充电状态失败: {e}")
            return False

    def get_soc(self):
        voltage = self.get_voltage()
        if voltage is None:
            return None

        charging = self.is_charging()

        if charging and voltage > self.charge_threshold:
            return 100

        if voltage > self.v_full:
            return 100
        elif voltage > self.v_half:
            return int(((voltage - self.v_half) / (self.v_full - self.v_half)) * 50 + 50)
        elif voltage > self.v_empty:
            return int(((voltage - self.v_empty) / (self.v_half - self.v_empty)) * 50)
        else:
            return 0

    def _soc_monitor_thread(self):
        while True:
            soc_samples = []
            for _ in range(10):
                soc = self.get_soc()
                if soc is not None:
                    soc_samples.append(soc)
                time.sleep(1)

            if soc_samples:
                new_avg = sum(soc_samples) // len(soc_samples)
                charging = self.is_charging()

                if not charging and new_avg > self.avg_soc:
                    pass
#                     print("[syscore_power] 未充电，SOC保持不变")
                else:
                    self.avg_soc = new_avg
#                     print(f"[syscore_power] 更新平均SOC: {self.avg_soc}%")
