import sys, io, re

def report_exception(e, context="未知错误", model_dir="/"):
    buf = io.StringIO()
    sys.print_exception(e, buf)
    detail = buf.getvalue()

    errorinfo = []
    errorinfo.append(f"{context}")
    errorinfo.append("--------------------------------------------------")

    lines = detail.splitlines()
    file_lines = [line for line in lines if line.strip().startswith("File")]

    if file_lines:
        errorinfo.append("错误调用链：")
        for line in file_lines:
            match = re.search(r'File "(.+)", line (\d+), in (.+)', line)
            if match:
                filename = match.group(1)
                lineno = match.group(2)
                funcname = match.group(3)
                errorinfo.append(f"→ {filename}, 第{lineno}行, 函数 {funcname}")
            else:
                errorinfo.append(f"→ 无法解析：{line}")
    else:
        errorinfo.append(f"错误位置：{model_dir}/（无 traceback 文件信息）")

    if len(lines) > 0:
        errorinfo.append(f"摘要：{lines[0]}")
    if len(lines) > 2:
        errorinfo.append(lines[-1])

    return errorinfo
