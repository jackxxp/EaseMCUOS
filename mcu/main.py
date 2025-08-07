model_dir = "/"
model_name = "main.py"
#版本信息
mainver , mainupdatedate = 1.0 , 20250807
print("<main> 信息 ------------------------------------------------------\n<main> 信息 系统启动 main.py 运行 版本",str(mainver),"更新日期",str(mainupdatedate))
import sys,time,io,re
print("<main> 信息 解释器信息：",sys.version)
try:
    with open("/conf/debug.conf", 'r') as file:
        content = file.read()
        if content =="1":
            debug = 1
            print("<main> 信息 调试模式开启")
        else:
            debug = 0
except Exception as e:
    debug = 0
#加载模块
#HMI
print("<main> 信息 加载硬件模块")
sys.path.append("/hardware")
import hw_hmi
hmi = hw_hmi.SerialDisplay(debug)
import hw_key
key = hw_key.DualButtonWithLED(debug)
#启动
hmi.tx("rest")
time.sleep(1.5)
hmi.tx("page sysload")
key.setled(10,500)
hmi.tx('bootlog.txt="按下主按键进入BASIC模式"')
bootjd=0
while bootjd !=100:
    bootjd +=1
    time.sleep(0.01)    
    hmi.tx(f'bootjd.val={bootjd}')
key.setled(10000,3000)
try:
    if not key.getmainkey():
        print("<main> 信息 启动EaseMCUOS")
        try:
            with open("/conf/startos.conf", 'r') as file:
                bootos = file.read()
                print(f"<main> 信息 启动槽位 {bootos}")
                hmi.tx(f'bootlog.txt="启动槽位 {bootos}"')
        except Exception as e:
            bootos = "1"
            print(f"<main> 警告 读取默认启动槽位槽位 {e}")
            hmi.tx(f'bootlog.txt="警告 读取默认启动槽位槽位 {e}"')
            time.sleep(1)
            print(f"<main> 信息 启动槽位 1")
            hmi.tx(f'bootlog.txt="启动槽位 1"')
        if bootos == "1" or bootos == "2" or bootos == "3" or bootos == "4":
            pass
        else:
            print(f"<main> 警告 读取默认启动槽位槽位错误 非法的槽位")
            hmi.tx(f'bootlog.txt="警告 读取默认启动槽位槽位错误 非法的槽位"')
            time.sleep(1)
            print(f"<main> 信息 启动槽位 1")
            hmi.tx(f'bootlog.txt="启动槽位 1"')
            bootos = "1"
        sys.path.append(f"/easemcuos/os{bootos}")
        os_main = __import__("os_main")
        os_main.main(f"/easemcuos/os{bootos}", hmi, key)
        
    else:
        print("<main> 信息 进入BASIC 模式")
        sys.path.append("/basic")
        import basic_main
        basic_main.main(hmi)
        
except Exception as e:
    buf = io.StringIO()
    sys.print_exception(e, buf)   # 写入
    detail = buf.getvalue()       # 读取
    print("<main> 错误 系统/Basic Mode错误：", detail)

    # 页面跳转与错误提示
    hmi.tx("page api_syserr")
    hmi.tx('errinfo.txt=""')

    detaillines = detail.splitlines()

    # ✅ 提取所有 traceback 中的文件位置行
    file_lines = [line for line in detaillines if line.strip().startswith("File")]
    if file_lines:
        hmi.tx(f'errinfo.txt+="\r\n错误调用链："')
        for line in file_lines:
            match = re.search(r'File "(.+)", line (\d+), in (.+)', line)
            if match:
                filename = match.group(1)
                lineno = match.group(2)
                funcname = match.group(3)
                hmi.tx(f'errinfo.txt+="\r\n→ {filename}, 第{lineno}行, 函数 {funcname}"')
            else:
                hmi.tx(f'errinfo.txt+="\r\n→ 无法解析：{line}"')
    else:
        hmi.tx(f'errinfo.txt+="\r\n错误位置：{model_dir}/（无 traceback 文件信息）"')

    # ✅ 显示首行和末行摘要
    if len(detaillines) > 0:
        hmi.tx(f'errinfo.txt+="\r\n摘要：{detaillines[0]}"')
    if len(detaillines) > 2:
        hmi.tx(f'errinfo.txt+="\r\n{detaillines[-1]}"')


