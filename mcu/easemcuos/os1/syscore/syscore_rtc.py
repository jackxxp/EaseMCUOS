# syscore_rtc.py
import machine,time,sys

rtc = machine.RTC()

def gettime(as_string=False):
    """
    获取当前 RTC 时间。
    返回格式：
        - as_string=True: "2025-08-07 19:51:00"
        - as_string=False: (year, month, day, weekday, hour, minute, second, subseconds)
    """
    t = rtc.datetime()
    if as_string:
        return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[4]:02d}:{t[5]:02d}:{t[6]:02d}"
    return t

def settime(year, month, day, hour, minute, second):
    """
    设置 RTC 时间。
    weekday 和 subseconds 自动设为 0。
    """
    try:
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
        return "ok"
    except Exception as e:
        return f"设置失败: {e}"

def gettimestamp():
    """
    返回当前时间的 UNIX 时间戳（秒）。
    注意：MicroPython 不自带 time.mktime()，需手动计算。
    """
    import time
    t = rtc.datetime()
    try:
        return time.mktime((t[0], t[1], t[2], t[4], t[5], t[6], 0, 0))
    except Exception as e:
        return f"转换失败: {e}"

def setfromtimestamp(ts):
    """
    使用 UNIX 时间戳设置 RTC 时间。
    """
    import time
    try:
        t = time.localtime(ts)
        return settime(t[0], t[1], t[2], t[3], t[4], t[5])
    except Exception as e:
        return f"设置失败: {e}"
def hmirtctomcurtc(hmi,osdir):
    sys.path.append(f"{osdir}/sysapi")
    import sysapi_hmihextoint
    rtcback=[0,0,0,0,0,0]
    hmi.tx('get rtc0')
    time.sleep(0.1)
    rtcback[0] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))
    hmi.tx('get rtc1')
    time.sleep(0.1)
    rtcback[1] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))
    hmi.tx('get rtc2')
    time.sleep(0.1)
    rtcback[2] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))
    hmi.tx('get rtc3')
    time.sleep(0.1)
    rtcback[3] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))
    hmi.tx('get rtc4')
    time.sleep(0.1)
    rtcback[4] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))
    hmi.tx('get rtc5')
    time.sleep(0.1)
    rtcback[5] = sysapi_hmihextoint.parse_hex_data(hmi.rx("return"))        
    settime(year=rtcback[0], month=rtcback[1], day=rtcback[2], hour=rtcback[3], minute=rtcback[4], second=rtcback[5])
    print(f"<oscorertc> 信息 同步后RTC时间{gettime()}")
    
    