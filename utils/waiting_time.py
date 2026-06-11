"""Simple waiting interval for the behavioral version."""

from psychopy import core, event


def waiting_time(param, second_to_wait):
    """Wait for a fixed duration without recording gaze, pupil, or frame data."""
    timer = core.Clock()
    while timer.getTime() < second_to_wait:
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            param['win'].close()
            core.quit()
        core.wait(0.01)
    return param
