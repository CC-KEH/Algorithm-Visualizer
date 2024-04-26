from themes.colors import *

def h_score(p1, p2):
    """Calculate heuristic using Manhattan distance

    Args:
        p1 (x,y): coordinates of point1
        p2 (x,y): coordinates of point2
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def update_info_screen(win,obj,color=BLACK,text1="",text2="",text3=""):
    if text1 != "":
        obj.set_text1(text1)
    if text2 != "":
        obj.set_text2(text2)
    if text3 != "":
        obj.set_text3(text3)
    obj.draw(win,color)