"""
Get screen details and initialize PsychoPy window
Converted from getScreenDetails.m
"""

from psychopy import visual, core, event, monitors


def get_screen_details():
    """
    Initialize PsychoPy window and get screen parameters

    Returns:
    --------
    param : dict
        Dictionary with window and screen parameters
    """
    param = {}

    # Create window (equivalent to PTB Screen)
    param['win'] = visual.Window(
        size=[2240, 1260],  # Use actual screen size from your error
        fullscr=True,       # Set to False for testing (easier to debug)
        screen=0,            # Use primary screen (changed from 1 to 0)
        color=[-1, -1, -1],  # Black background (PsychoPy uses -1 to 1 range)
        colorSpace='rgb',
        units='pix',
        allowGUI=False,       # Allow GUI for easier debugging
        monitor='testMonitor'
    )
    # param['win'] = visual.Window(
    #     fullscr=True,
    #     screen=0,
    #     color=[-1, -1, -1],
    #     colorSpace='rgb',
    #     units='pix',
    #     allowGUI=False,  # usually False for fullscreen experiments
    #     monitor='testMonitor'
    # )

    # Get window size
    param['screen_x_pixels'] = param['win'].size[0]
    param['screen_y_pixels'] = param['win'].size[1]
    param['x_center'] = param['screen_x_pixels'] / 2
    param['y_center'] = param['screen_y_pixels'] / 2

    # Frame timing
    param['ifi'] = 1.0 / 60.0  # Inter-frame interval (assuming 60 Hz)
    param['wait_frames'] = 1

    # IMPORTANT: Show mouse cursor
    param['win'].mouseVisible = True

    def quit_experiment():
        param['win'].close()
        core.quit()

    event.globalKeys.clear()
    event.globalKeys.add(key='escape', func=quit_experiment)

    print(f"✓ Window created: {param['screen_x_pixels']}x{param['screen_y_pixels']}")

    return param
