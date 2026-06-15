from click import style

def success(msg): return style(msg, fg="green")
def error(msg): return style(msg, fg="red")
def warn(msg): return style(msg, fg="yellow")
def info(msg): return style(msg, fg="blue")
