import matplotlib
import matplotlib.colors as mc
import colorsys


def adjust_lightness(color, amount=0.5):
    if color is None:
        return None

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return matplotlib.colors.to_hex(colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2]))


def adjust_saturation(color, amount=0.5):
    if color is None: return None
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return matplotlib.colors.to_hex(colorsys.hls_to_rgb(c[0], c[1], max(0, min(1, amount * c[2]))))
