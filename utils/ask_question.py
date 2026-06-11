"""
Ask question and collect a mouse-click rating response.
"""

import numpy as np
from psychopy import core, event, visual
from configs.get_param_for_drawing import get_param_for_drawing
from show_example_images import show_example_images
from show_question_images import show_question_images
from waiting_time import waiting_time
from configs.setting_mouse import setting_mouse


def wait_with_escape(param, seconds):
    timer = core.Clock()
    while timer.getTime() < seconds:
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            param['win'].close()
            core.quit()
        core.wait(0.01)


def draw_rating_buttons(param, random_start_angle, selected_idx=None):
    """
    Draw rating buttons.

    selected_idx is zero-based.
    If selected_idx is not None, draw a border around the selected button.
    """
    button_centers = []
    button_positions = []

    for i in range(param['num_buttons']):
        if param['scoring_order'][param['question_num'] - 1]:
            angle = random_start_angle + i * (2 * np.pi / param['num_buttons'])
        else:
            angle = random_start_angle - i * (2 * np.pi / param['num_buttons'])

        button_center_x = param['center_x'] + param['big_radius'] * np.cos(angle)
        button_center_y = param['center_y'] + param['big_radius'] * np.sin(angle)

        button_x = button_center_x - param['screen_x_pixels'] / 2
        button_y = -button_center_y + param['screen_y_pixels'] / 2

        circle = visual.Circle(
            param['win'],
            radius=param['small_radius'],
            pos=[button_x, button_y],
            fillColor=param['grey'],
            lineColor=param['black'],
            lineWidth=5,
        )
        circle.draw()

        text = visual.TextStim(
            param['win'],
            text=str(i + 1),
            pos=[button_x, button_y],
            height=50,
            color=param['black'],
        )
        text.draw()

        button_centers.append([button_center_x, button_center_y])
        button_positions.append([button_x, button_y])

    if selected_idx is not None:
        selected_x, selected_y = button_positions[selected_idx]

        selected_border = visual.Circle(
            param['win'],
            radius=param['small_radius'] + 8,
            pos=[selected_x, selected_y],
            fillColor=None,
            lineColor=param['white'],
            lineWidth=6,
        )
        selected_border.draw()

    return button_centers


def ask_question(param):
    """
    Display question images and collect one rating response.

    Only the selected rating and reaction time are appended to param['data'].
    Mouse trajectory, gaze, pupil, and frame-level timing are not recorded.
    """
    param = get_param_for_drawing(param)

    param = show_example_images(param)
    param = show_question_images(param)
    param = waiting_time(param, 2.0)

    random_start_angle = np.random.rand() * 2 * np.pi

    print(f"Trial: {param['question_num']}_{param['sub_trial']}")

    setting_mouse(param)
    mouse = event.Mouse(win=param['win'])
    mouse.clickReset()

    score_num = 0
    param['win'].mouseVisible = True
    starting_time = core.getTime()

    while True:
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            param['win'].close()
            core.quit()

        x, y = mouse.getPos()
        buttons = mouse.getPressed()

        x_screen = x + param['screen_x_pixels'] / 2
        y_screen = -y + param['screen_y_pixels'] / 2

        button_centers = draw_rating_buttons(
            param=param,
            random_start_angle=random_start_angle,
            selected_idx=None,
        )

        param['win'].flip()

        if buttons[0]:
            for i, center in enumerate(button_centers):
                dist = np.sqrt((x_screen - center[0]) ** 2 + (y_screen - center[1]) ** 2)

                if dist < param['small_radius']:
                    score_num = i + 1
                    ending_time = core.getTime()

                    # RT는 여기서 이미 확정됨.
                    # 아래 0.5초 feedback 시간은 RT에 포함되지 않음.
                    draw_rating_buttons(
                        param=param,
                        random_start_angle=random_start_angle,
                        selected_idx=i,
                    )
                    param['win'].flip()
                    wait_with_escape(param, 0.5)

                    while mouse.getPressed()[0]:
                        keys = event.getKeys(['escape'])
                        if 'escape' in keys:
                            param['win'].close()
                            core.quit()
                        core.wait(0.01)
                    wait_with_escape(param, 0.05)

                    trial_data = [
                        param['trial_counter'],
                        param['question_num'],
                        param['sub_trial'] + 1,
                        score_num,
                        ending_time - starting_time,
                    ]
                    param['data'].append(trial_data)
                    return param

        core.wait(0.01)
