"""
Draw dashed lines on screen - OPTIMIZED to match image positions
Converted from drawDashedLines.m
"""

import numpy as np
from psychopy import visual


def draw_dashed_lines(param, color_left, color_right):
    """
    Draw dashed vertical lines on the screen, matching image heights

    Parameters:
    -----------
    param : dict
        Experiment parameters containing:
        - win: PsychoPy window
        - x_line_left_example: x position for left example line
        - x_line_right_example: x position for right example line
        - x_line_left_question: x position for left question line
        - x_line_right_question: x position for right question line
        - img_rects_example: rectangles for example images
        - img_rects_question: rectangles for question images
        - screen_x_pixels: screen width
        - screen_y_pixels: screen height
    color_left : list
        RGB color for left lines [r, g, b]
    color_right : list
        RGB color for right lines [r, g, b]

    Returns:
    --------
    param : dict
        Unchanged parameter dictionary (returned for consistency)
    """
    # OPTIMIZED: Calculate line positions based on actual image positions
    # This makes lines match the vertical span of the images

    # Get the top and bottom positions from image rectangles
    if 'img_rects_example' in param and len(param['img_rects_example']) > 0:
        # Find min and max Y positions from all images
        all_rects = param['img_rects_example'] + param['img_rects_question']

        y_positions_top = [rect[1] for rect in all_rects]  # All top positions
        y_positions_bottom = [rect[3] for rect in all_rects]  # All bottom positions

        y_top = min(y_positions_top) - 20  # Add small margin
        y_bottom = max(y_positions_bottom) + 20
    else:
        # Fallback to screen-based positioning
        y_top = param['screen_y_pixels'] * 0.15
        y_bottom = param['screen_y_pixels'] * 0.85

    dash_length = 20
    gap = 10
    line_width = 3

    # Calculate y positions for dashes - only within image range
    y_positions = np.arange(0, param['screen_y_pixels'], dash_length + gap)

    # Draw left example lines (vertical dashed)
    for y in y_positions:
        # Convert to PsychoPy coordinates (center-based)
        x_psy = param['x_line_left_example'] - param['screen_x_pixels'] / 2
        y_start_psy = -(y - param['screen_y_pixels'] / 2)
        y_end_psy = -((y + dash_length) - param['screen_y_pixels'] / 2)

        line = visual.Line(
            param['win'],
            start=[x_psy, y_start_psy],
            end=[x_psy, y_end_psy],
            lineColor=color_left,
            lineWidth=line_width
        )
        line.draw()

    # Draw left question lines (vertical dashed)
    for y in y_positions:
        x_psy = param['x_line_left_question'] - param['screen_x_pixels'] / 2
        y_start_psy = -(y - param['screen_y_pixels'] / 2)
        y_end_psy = -((y + dash_length) - param['screen_y_pixels'] / 2)

        line = visual.Line(
            param['win'],
            start=[x_psy, y_start_psy],
            end=[x_psy, y_end_psy],
            lineColor=color_right,
            lineWidth=line_width
        )
        line.draw()

    # Draw right example lines (vertical dashed)
    for y in y_positions:
        x_psy = param['x_line_right_example'] - param['screen_x_pixels'] / 2
        y_start_psy = -(y - param['screen_y_pixels'] / 2)
        y_end_psy = -((y + dash_length) - param['screen_y_pixels'] / 2)

        line = visual.Line(
            param['win'],
            start=[x_psy, y_start_psy],
            end=[x_psy, y_end_psy],
            lineColor=color_left,
            lineWidth=line_width
        )
        line.draw()

    # Draw right question lines (vertical dashed)
    for y in y_positions:
        x_psy = param['x_line_right_question'] - param['screen_x_pixels'] / 2
        y_start_psy = -(y - param['screen_y_pixels'] / 2)
        y_end_psy = -((y + dash_length) - param['screen_y_pixels'] / 2)

        line = visual.Line(
            param['win'],
            start=[x_psy, y_start_psy],
            end=[x_psy, y_end_psy],
            lineColor=color_right,
            lineWidth=line_width
        )
        line.draw()

    return param