import machine
import time

class SerialDisplay:
    def __init__(self):
        # 初始化 UART 串口，配置波特率、数据位、奇偶校验、停止位以及 TX 和 RX 引脚
        self.uart = machine.UART(1, baudrate=921600, bits=8, parity=None, stop=1, tx=40, rx=39)
        print("UART 初始化成功")
        # 初始化缓冲区
        self.buffer = b''

    def tx(self, info):
        # 发送信息，追加结束标记
        data = info.encode() + b'\xff' * 3
        print(f"发送数据: {data}")
        self.uart.write(data)

    def run(self):
        # 如果有可用的串口数据
        if self.uart.any():
            data = self.uart.read(self.uart.any())
            print(f"收到数据 (Hex): {data.hex()}")
            self.buffer += data

        # 定义命令的起始和结束标记
        start_marker = b"|cmd|"
        end_marker = b"|end|"
        # 查找起始标记和结束标记的位置
        start = self.buffer.find(start_marker)
        end = self.buffer.find(end_marker)

        # 如果找到完整的命令
        if start != -1 and end != -1 and end > start:
            # 提取命令内容（从起始标记后到结束标记前）
            command = self.buffer[start + len(start_marker):end]
            # 移除缓冲区中已处理的命令部分（包括起始标记和结束标记）
            self.buffer = self.buffer[end + len(end_marker):]
            # 解码命令内容为 UTF-8 格式的字符串
            try:
                decoded_command = command.decode('utf-8')
                print(f"收到命令: {decoded_command}")
                return decoded_command
            except Exception as e:
                print(f"命令解码失败: {e}")
                return None
        # 如果没有找到完整的命令，返回 None
        return None

# 示例使用
if __name__ == "__main__":
    display = SerialDisplay()
    display.tx("page basic")
    while True:
        time.sleep(0.01)
        command = display.rx()
        if command:
            print(f"处理命令: {command}")