#版本信息
hmiver , hmiupdatedate = 1.0 , 20250807

import machine
import _thread
import time
import sys
import io

class SerialDisplay:
    PREFIXES = {
        b'|b|'    : 'b',
        b'|ctrl|' : 'ctrl',
        b'|input|': 'input',
        b'|more|' : 'more'
    }

    def __init__(self, debug=0):
        
        self.hmiuart = machine.UART(1, baudrate=921600,
                                    bits=8, parity=None, stop=1,
                                    tx=40, rx=39)
        self.debug = debug

        # 线程安全数据槽
        self._lock = _thread.allocate_lock()
        self._data = {k: None for k in list(self.PREFIXES.values()) + ['return']}

        self._buf   = b''
        self._stamp = time.ticks_ms()

        # 启动后台线程
        _thread.start_new_thread(self._bg_run, ())
        print("<hmi> 信息 版本:" + str(hmiver) + " 更新日期:" + str(hmiupdatedate))

    # ---------- 后台线程 ----------
    def _bg_run(self):
        while True:
            try:
                if self.hmiuart.any():
                    chunk = self.hmiuart.read(self.hmiuart.any())
                    if self.debug:
                        print(f"<hmi> 调试 HMI==>MCU:{chunk}")
                    with self._lock:
                        self._buf += chunk
                with self._lock:
                    self._parse_locked()
            except Exception as e:
                self._print_error(e)
            time.sleep_ms(10)

    # ---------- 解析 ----------
    def _parse_locked(self):
        try:
            # 1) 前缀 + |end|
            for prefix, tag in self.PREFIXES.items():
                if self._buf.startswith(prefix):
                    after   = len(prefix)
                    end_pos = self._buf.find(b'|end|', after)
                    if end_pos == -1:
                        continue
                    payload = self._buf[after:end_pos]
                    self._buf = self._buf[end_pos + 5:]
                    self._data[tag] = payload
                    self._stamp = time.ticks_ms()
                    return

            # 2) 无前缀 + \xff\xff\xff
            end_pos = self._buf.find(b'\xff\xff\xff')
            if end_pos != -1:
                payload = self._buf[:end_pos]
                self._buf = self._buf[end_pos + 3:]
                self._data['return'] = payload
                self._stamp = time.ticks_ms()
                return

            # 3) 超时清理
            if time.ticks_diff(time.ticks_ms(), self._stamp) > 1000 and self._buf:
                print(f"<hmi> 警告:无法解析数据:{self._buf}")
                self._buf = b''
                self._stamp = time.ticks_ms()
        except Exception as e:
            self._print_error(e)

    # ---------- 发送 ----------
    def tx(self, info):
        try:
            data = info.encode() + b'\xff\xff\xff'
            if self.debug:
                print(f"<hmi> 调试 MCU==>HMI:{data}")
            self.hmiuart.write(data)
            return "ok"
        except Exception as e:
            self._print_error(e)
            return f"error {e}"

    def tx_hex(self, hex_str: str, auto_end: bool = True):
        """
        hex_str : 十六进制字符串，可带空格可不带
                  例: "A5 5A 01" 或 "A55A01"
        auto_end: True  自动追加 b'\xff\xff\xff'
                  False 不追加
        """
        try:
            payload = bytes.fromhex(hex_str.replace(" ", ""))
            data = payload + (b'\xff\xff\xff' if auto_end else b'')
            if self.debug:
                print(f"<hmi> 调试 MCU==>HMI(hex):{data.hex()}")
            self.hmiuart.write(data)
            return "ok"
        except ValueError as e:
            print(f"<hmi> Warn:tx_hex 格式错误 -> {e}")
            return f"error {e}"
        except Exception as e:
            self._print_error(e)
            return f"error {e}"

    # ---------- 线程安全读 ----------
    def rx(self, key):
        if key not in self._data:
            return ""
        try:
            with self._lock:
                val = self._data[key]
                self._data[key] = None

            if val is None:
                return ""

            # 对 return 直接返回 hex
            if key == 'return':
                return str(val.hex())

            # 其余前缀尝试 UTF-8 解码
            try:
                return val.decode('utf-8')
            except UnicodeDecodeError:
                print(f"<hmi> Warn:解码失败，返回 hex:{val.hex()}")
                return val.hex()

        except Exception as e:
            self._print_error(e)
            return f"error {e}"
    # ---------- 统一错误打印 ----------
    @staticmethod
    def _print_error(e):
        buf = io.StringIO()
        sys.print_exception(e, buf)
        detail = buf.getvalue()
        print("<hmi> Error:", detail.rstrip())

# #---------------- DEMO ----------------
# if __name__ == "__main__":
#     disp = SerialDisplay(debug=1)
#     disp.tx("get rtc1")
#     while True:
#         for k in ('b', 'ctrl', 'input', 'more', 'return'):
#             txt = disp.rx(k)
#             if txt:
#                 print(f"收到[{k}]: {txt}")
#         time.sleep(0.1)