from themes.colors import *
import numpy as np
import simpleaudio as sa
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
    
def play_sound(frequency, duration=0.01):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    audio = tone * (2**15 - 1) / np.max(np.abs(tone))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()
    