colors = {
    'moved': (0, 0, 255),
    'listener': (255, 0, 0),
    'identificate': (0, 255, 0),
}

def get_color(action):
    return colors.get(action, (0, 0, 0))