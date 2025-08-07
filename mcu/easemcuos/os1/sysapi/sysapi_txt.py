# sysapi_txt.py

def readtxt(path):
    try:
        with open(path, "r") as f:
            return "ok",f.read()
    except Exception as e:
        return f"读取失败: {e}",None

def writetxt(path, txt, overwrite=False):
    try:
        mode = "w" if overwrite else "a"
        with open(path, mode) as f:
            f.write(txt)
        return "ok"
    except Exception as e:
        return f"写入失败: {e}"

def readtxtline(path, line):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        if line-1 < 0 or line-1 >= len(lines):
            return f"读取失败: 行号 {line-1} 超出范围",None
        return "ok",lines[line-1].rstrip('\n')
    except Exception as e:
        return f"读取失败: {e}",None

def writetxtline(path, line, txt):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        return f"写入失败: 文件不存在或无法读取 ({e})"

    try:
        # 扩展文件行数以支持写入新行
        while len(lines) <= line:
            lines.append("\n")
        lines[line] = txt + "\n"
        with open(path, "w") as f:
            f.writelines(lines)
        return "ok"
    except Exception as e:
        return f"写入失败: {e}"
    
def appendtxt(path, txt, newline=True):
    try:
        with open(path, "a") as f:
            f.write(txt + ("\n" if newline else ""))
        return "ok"
    except Exception as e:
        return f"续写失败: {e}"


