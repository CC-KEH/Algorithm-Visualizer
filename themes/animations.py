from themes.themes import *

def visit_animation(visited,theme_type):
    for node in visited:
        if node.color == themes[theme_type]["closed_color_1"] or node.color == themes[theme_type]["closed_color_3"]:
            visited.remove(node)
            continue
        r, g, b = node.color
        if g < 255:
            g += 1
        node.color = (r, g, b)


def visit_animation2(node,theme_type):
    if node.color == themes[theme_type]["closed_color_1"]:
        return True
    else:
        r, g, b = node.color
        b += 1
        node.color = (r, g, b)
        return False
    
def path_animation(path,theme_type):
    for node in path:
        if not node.is_start():
            r, g, b = node.color
            if node.dec_animation:
                g -= 1
                if g <= themes[theme_type]["path_color_1"][1]:
                    node.dec_animation = False
            else:
                g += 1
                if g >= themes[theme_type]["path_color_2"][1]:
                    node.dec_animation = True
        node.color = (r, g, b)