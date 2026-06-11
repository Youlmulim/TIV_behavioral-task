"""
Initialize mouse position
Converted from settingMouse.m
"""

from psychopy import event


def setting_mouse(param):
    """
    Initialize mouse position to center of screen
    
    Parameters:
    -----------
    param : dict
        Experiment parameters containing:
        - win: PsychoPy window object
        - screen_x_pixels: screen width in pixels
        - screen_y_pixels: screen height in pixels
        
    Notes:
    ------
    In MATLAB PsychToolbox:
        SetMouse(param.screenXpixels *0.5, param.screenYpixels * 0.5, param.window);
    
    In PsychoPy:
        Mouse position (0, 0) is already at the center
        Coordinate system is center-based, not top-left based
    """
    # Create or get mouse object
    mouse = event.Mouse(win=param['win'])
    
    # Flip to update display
    param['win'].flip()

