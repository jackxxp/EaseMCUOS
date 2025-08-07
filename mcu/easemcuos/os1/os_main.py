model_name = "os_main.py"

import sys

def main(osdir,hmi,key):
    os_dir= osdir
    print(f"<osmain> 信息 EaseMCUOS启动 位置{os_dir}")
    hmi.tx("page sysload")
    hmi.tx(f'bootlog.txt="EaseMCUOS启动 位置{os_dir}"')
    print(f"<osmain> 信息 加载系统内核oscore")
    sys.path.append(f"{os_dir}/syscore")
    oscoreapi = __import__("syscore_main")
    oscoreapi.oscore(os_dir,hmi,key)

