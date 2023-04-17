import time



INFO = 0
WARNING = 1
DANGER = 2
ERROR = 3
SUCCESS = 4


def getWithColor(t, c="n", b="n"):
    color = {
        "n": "0",
        "red": "31", "black": "30", "green": "32", "yellow": "33", "blue": "34", "white": "37",
        "bblack": "40", "bred": "41", "bgreen": "42", "byellow": "43", "bblue": "44", "bwhite": "47",
        "purple": "35", "bpurple": "45",
        # 增加几个特殊的

    }
    if b == 'n':
        left = "\033[1;" + color[c] + "m"
    else:
        left = "\033[1;" + color[c] + ";" + color[b] + "m"

    right = "\033[0m"

    return left + t + right


def printWithColor(t, c="n", b="n"):
    content = getWithColor(t, c, b)
    print(content, '\n', end='')


def log(tag="Coolapk", t=None, risk=INFO):
    text = time.strftime("[%Y-%m-%d %H:%M:%S] " + tag + " >>> ", time.localtime()) + str(t)
    if risk == DANGER:
        printWithColor(text, "purple")
    elif risk == WARNING:
        printWithColor(text, "yellow")
    elif risk == ERROR:
        printWithColor(text, "red", "bblack")
    elif risk == SUCCESS:
        printWithColor(text, "green")
    elif risk == INFO:
        printWithColor(text, "blue")
