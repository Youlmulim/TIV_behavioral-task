"""Display waiting screen and proceed by mouse click."""

from psychopy import visual, event, core
from utils.handle_fixation import handle_fixation


def waiting_screen(param, first_start=False):
    """
    Display a waiting screen.

    The initial start screen and the pre-trial center target both use mouse
    clicks, keeping the task behavior-only and mouse-click-based.
    """
    mouse = event.Mouse(win=param['win'])

    if first_start:
        text = visual.TextStim(
            param['win'],
            text='Click to Start',
            height=100,
            color=param['white'],
            font='Arial',
        )
        mouse.clickReset()
        while True:
            text.draw()
            param['win'].flip()

            keys = event.getKeys(['escape'])
            if 'escape' in keys:
                param['win'].close()
                core.quit()

            if mouse.getPressed()[0]:
                while mouse.getPressed()[0]:
                    keys = event.getKeys(['escape'])
                    if 'escape' in keys:
                        param['win'].close()
                        core.quit()
                    core.wait(0.01)
                break
            core.wait(0.01)

    # Center click target before every trial.
    circle = visual.Circle(
        param['win'],
        radius=param['circle_radius'],
        pos=[0, 0],
        fillColor=param['blue'],
        lineColor=param['blue'],
    )
    circle.draw()
    param['win'].flip()

    param = handle_fixation(param, param['center_x'], param['center_y'], None)

    return param
