model_dir = "/basic"
model_name = "basic_main.py"
#版本信息
basicver , basicupdatedate = 1.0 , 20250807
import time,machine

def reboot_system(hmi):
    print("<basic> 信息 系统重启")
    hmi.tx("page api_wait")
    hmi.tx('title.txt="重启"')
    time.sleep(0.1)
    hmi.tx('info.txt="正在重启系统，请稍后"')
    machine.reset()

def main(hmi):
    print("<basic> 信息 Basic Mode运行 版本",str(basicver),"更新日期",str(basicupdatedate))
    while 1 :
        backhome = 0
        time.sleep(0.1)
        hmi.tx("page basic")
        while not backhome:
            time.sleep(0.1)
            hmi.tx(f'title.txt="Basic Mode                 ver:{str(basicver)}         更新时间:{str(basicupdatedate)}"')
            hmi.tx(f'info.txt="配置信息"')
            try:
                with open("/conf/startos.conf", 'r') as file:
                    bootos = file.read()
                    hmi.tx(f'info.txt+="\r\n默认启动系统 槽位 {bootos}"')
            except Exception as e:
                hmi.tx(f'info.txt+="\r\n读取默认启动系统错误\r\n{e}"')       
            
            while not backhome:
                time.sleep(0.1)           
                hmi.tx(f'b0.txt="设置默认启动系统"')
                ctrlcmd = hmi.rx("ctrl")
                bcmd = hmi.rx("b")
                if ctrlcmd == "exit":
                    reboot_system(hmi)
                if bcmd == "0":
                    print("<basic> 信息 设置默认启动系统")
                    hmi.rx("b")     # 清除残留指令
                    hmi.rx("exit")  # 清除残留指令
                    hmi.tx('info.txt="请选择要设置成为默认的启动槽位"')
                    hmi.tx('b0.txt="取消"')
                    for i in range(1, 5):
                        hmi.tx(f'b{i}.txt="槽位 {i}"')

                    while 1:
                        time.sleep(0.1)
                        ctrlcmd = hmi.rx("ctrl")
                        bcmd = hmi.rx("b")

                        if ctrlcmd == "exit":
                            reboot_system(hmi)

                        if bcmd == "0":
                            backhome = 1
                            break

                        if bcmd in {"1", "2", "3", "4"}:
                            try:
                                with open("/conf/startos.conf", "w") as f:
                                    f.write(bcmd)
                                hmi.tx(f'info.txt+="\r\n设置成功 默认槽位 {bcmd}"')
                            except Exception as e:
                                hmi.tx(f'info.txt+="\r\n设置失败 {e}"')
                            time.sleep(2)
                            backhome = 1
                            break









