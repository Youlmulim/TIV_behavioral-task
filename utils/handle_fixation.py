"""
Mouse-hover based stimulus reveal.

The original eye-tracking version waited for gaze fixation. In this behavioral
version, the same target locations are used, but participants reveal each image
by hovering inside the target circle.
"""

import numpy as np
from psychopy import core, event


def handle_fixation(param, compare_x, compare_y, fixation_threshold=None):
    """
    Wait until the participant hovers inside the target circle.

    compare_x, compare_y are in screen coordinates with origin at the top-left,
    matching the coordinates used elsewhere in the converted MATLAB code.
    """
    mouse = event.Mouse(win=param['win'])
    radius = param['circle_radius'] + 130
    if fixation_threshold is None:
        fixation_threshold = param.get('fixation_threshold', 0.2)

    fixation_threshold = float(fixation_threshold)
    hover_clock = core.Clock()
    inside_target = False

    while True:
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            param['win'].close()
            core.quit()

        x, y = mouse.getPos()

        # Convert PsychoPy center-based coordinates to screen coordinates.
        x_screen = x + param['screen_x_pixels'] / 2
        y_screen = -y + param['screen_y_pixels'] / 2

        dist = np.sqrt((x_screen - compare_x) ** 2 + (y_screen - compare_y) ** 2)

        if dist < radius:
            if not inside_target:
                hover_clock.reset()
                inside_target = True

            if float(hover_clock.getTime()) >= fixation_threshold:
                timer = core.Clock()
                while timer.getTime() < 0.05:
                    keys = event.getKeys(['escape'])
                    if 'escape' in keys:
                        param['win'].close()
                        core.quit()
                    core.wait(0.01)
                break
        else:
            inside_target = False

        core.wait(0.01)

    return param
