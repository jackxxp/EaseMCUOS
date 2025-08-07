# os_appruntime.py


class SystemRuntimeManager:
    def __init__(self):
        self.initialized = False
        self.osdir = None
        self.running = False
        self.app_task = None
        self.bg_tasks = {}

    def init(self, osdir):
        if self.initialized:
            print("<osappruntime> 警告 已初始化，忽略重复调用")
            return
        self.osdir = osdir
        self.initialized = True
        print(f"<osappruntime> 信息 初始化完成，osdir = {osdir}")


# ✅ 全局实例（延迟初始化）
osapp = SystemRuntimeManager()
