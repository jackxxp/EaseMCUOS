model_dir = "/easemcuos/osx"
model_name = "os_main.py"
#版本信息
osver , osupdatedate = 1.0 , 20250807
def main(slot,hmi,key):
    model_dir= f"/easemcuos/os{slot}"
    print(f"<os> 信息 EaseMCUOS启动 槽位{slot} 版本{osver} 更新日期{osupdatedate}")
    print(3)