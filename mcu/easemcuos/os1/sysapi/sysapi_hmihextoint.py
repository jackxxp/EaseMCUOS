def parse_hex_data(hexstr):
    try:
        # 清理输入
        hexstr = hexstr.lower().strip()

        # 校验长度（必须至少10个字符）
        if len(hexstr) < 10:
            return "格式错误: HEX 长度不足"

        # 提取数据部分（跳过前缀1字节 = 2字符）
        data_hex = hexstr[2:10]  # 4字节数据 = 8字符

        # 转换为字节并解析为整数（小端模式）
        data_bytes = bytes.fromhex(data_hex)
        value = int.from_bytes(data_bytes, "little")

        return value
    except Exception as e:
        return 99999