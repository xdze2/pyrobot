

from pyrobot.rgb_leds import ColorMap, RgbColor


def test_ColorMap():

    cm = ColorMap(0, 100, 'gist_heat')
    print( cm.get_rgb(50.5) )
    
    assert RgbColor(193, 2, 0) == cm.get_rgb(50.5)