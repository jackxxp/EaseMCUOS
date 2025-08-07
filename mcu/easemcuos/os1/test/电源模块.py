import sys,time
sys.path.append("/easemcuos/os1/syscore")
from syscore_power import Battery

battery = Battery()

while 1:
    print("电压:", battery.get_voltage(), "V")
    print("是否充电:", battery.is_charging())
    print("电量百分比:", battery.get_soc(), "%")
    print("平均SOC:",battery.avg_soc,"%")
    time.sleep(1)
