#版本信息
oscorever , oscoreupdatedate = 1.0 , 20250807

import sys,time

class oscore:
    def __init__(self, osdir,hmi,key):
        print("<oscore> 信息 版本:" + str(oscorever) + " 更新日期:" + str(oscoreupdatedate))
        self.osdir = osdir
        self.hmi = hmi
        self.key = key
        self.hmi.tx('bootjd.val=5')
        sys.path.append(f"{self.osdir}/syscore")
        sys.path.append(f"{self.osdir}/sysapi")
        sys.path.append(f"{self.osdir}") 
        self.hmi.tx('bootlog.txt="加载RTC模块"')
        print("<oscore> 信息 加载RTC模块")
        self.rtc = __import__("syscore_rtc")
        self.hmi.tx('bootlog.txt="设置MCU RTC"')
        print("<oscore> 信息 设置MCU RTC")
        self.rtc.hmirtctomcurtc(self.hmi,self.osdir)
        self.hmi.tx(f'bootlog.txt="同步后RTC时间{self.rtc.gettime()}"')
        self.hmi.tx('bootjd.val=10')
        self.hmi.tx('bootlog.txt="加载电源模块"')
        print("<oscore> 信息 加载电源模块")
        import syscore_power
        self.power = syscore_power.Battery()
        self.hmi.tx(f'bootlog.txt="初始电量估算 {self.power.avg_soc}%"')
        self.hmi.tx('bootjd.val=15')
        self.hmi.tx('bootlog.txt="加载应用运行模块"')
        print("<oscore> 信息 加载应用运行模块")
        from os_appruntime import osapp
        osapp.init(self.osdir)
        self.hmi.tx('bootlog.txt="加载应用运行模块成功"')
        self.hmi.tx('bootjd.val=100')        
        
        
        
        