"""
Get parameters for drawing stimuli
Converted from getParamForDrawing.m
"""

import numpy as np
from pathlib import Path
from get_img_texture import get_img_texture


def get_param_for_drawing(param):
    """
    Load and prepare image stimuli for current trial

    Parameters:
    -----------
    param : dict
        Experiment parameters

    Returns:
    --------
    param : dict
        Updated parameters with image textures and positions
    """
    # Set base path for images - UPDATED TO LOOK IN PROJECT ROOT
    # You can also change this to absolute path if needed
    base_path = Path('questions') / f'question{param["question_num"]}'

    # Check if directory exists
    if not base_path.exists():
        print(f"❌ ERROR: Image directory not found: {base_path.absolute()}")
        print(f"   Looking in: {Path.cwd()}")
        print(f"   Please ensure 'questions/question{param['question_num']}/' exists")
        raise FileNotFoundError(f"Image directory not found: {base_path}")

    # Get image names from randomized pairs
    example_img = param['randomized_question_pairs'][param['sub_trial']][0]
    question_img = param['randomized_question_pairs'][param['sub_trial']][1]

    param['parts_example'] = example_img.split('_')
    param['parts_question'] = question_img.split('_')

    # Create full image names
    example_names = [example_img, f"{param['parts_example'][0]}_2"]
    question_names = [question_img, f"{param['parts_question'][0]}_2"]

    # Construct image paths
    image_paths_example = [base_path / f"{name}.png" for name in example_names]
    image_paths_question = [base_path / f"{name}.png" for name in question_names]

    # Check if images exist
    for img_path in image_paths_example + image_paths_question:
        if not img_path.exists():
            print(f"❌ ERROR: Image file not found: {img_path}")
            raise FileNotFoundError(f"Image not found: {img_path}")

    print(f"✓ Found images for question {param['question_num']}, trial {param['sub_trial']}")

    # Set y positions
    y_pos_example = [
        param['screen_y_pixels'] * 0.35,
        param['screen_y_pixels'] * 0.65
    ]
    y_pos_question = [
        param['screen_y_pixels'] * 0.35,
        param['screen_y_pixels'] * 0.65
    ]

    # Set x positions based on left/right configuration.
    # question_num is stored as 1-indexed for human-readable output, so use
    # zero-indexing when accessing NumPy matrices.
    question_idx = param['question_num'] - 1
    if not param['left_right_matrix'][question_idx, param['sub_trial']]:  # example left
        x_pos_example = [param['screen_x_pixels'] * 0.35] * 15
        x_pos_question = [param['screen_x_pixels'] * 0.65] * 15
    else:  # example right
        x_pos_example = [param['screen_x_pixels'] * 0.65] * 15
        x_pos_question = [param['screen_x_pixels'] * 0.35] * 15

    # Load image textures
    param['img_textures_example'] = []
    param['img_rects_example'] = []
    param['img_textures_question'] = []
    param['img_rects_question'] = []

    for i in range(2):
        # Example images
        img_stim, dest_rect = get_img_texture(
            str(image_paths_example[i]),
            param['win'],
            x_pos_example[i],
            y_pos_example[i],
            param['sub_rect_width'],
            param['sub_rect_height']
        )
        param['img_textures_example'].append(img_stim)
        param['img_rects_example'].append(dest_rect)

        # Question images
        img_stim, dest_rect = get_img_texture(
            str(image_paths_question[i]),
            param['win'],
            x_pos_question[i],
            y_pos_question[i],
            param['sub_rect_width'],
            param['sub_rect_height']
        )
        param['img_textures_question'].append(img_stim)
        param['img_rects_question'].append(dest_rect)

    # Calculate centers and circles for example images
    param['center_x_example'] = []
    param['center_y_example'] = []
    param['small_circle_rect_example'] = []

    for i in range(len(param['img_textures_example'])):
        rect = param['img_rects_example'][i]
        bigger_rect = [
            rect[0] - param['expand'],
            rect[1] - param['expand'],
            rect[2] + param['expand'],
            rect[3] + param['expand']
        ]

        center_x = (rect[0] + rect[2]) / 2
        center_y = (rect[1] + rect[3]) / 2
        param['center_x_example'].append(center_x)
        param['center_y_example'].append(center_y)

        circle_rect = [
            center_x - param['circle_radius'],
            center_y - param['circle_radius'],
            center_x + param['circle_radius'],
            center_y + param['circle_radius']
        ]
        param['small_circle_rect_example'].append(circle_rect)

    param['x_line_left_example'] = bigger_rect[0]
    param['x_line_right_example'] = bigger_rect[2]

    # Calculate centers and circles for question images
    param['center_x_question'] = []
    param['center_y_question'] = []
    param['small_circle_rect_question'] = []

    for i in range(len(param['img_textures_question'])):
        rect = param['img_rects_question'][i]
        bigger_rect = [
            rect[0] - param['expand'],
            rect[1] - param['expand'],
            rect[2] + param['expand'],
            rect[3] + param['expand']
        ]

        center_x = (rect[0] + rect[2]) / 2
        center_y = (rect[1] + rect[3]) / 2
        param['center_x_question'].append(center_x)
        param['center_y_question'].append(center_y)

        circle_rect = [
            center_x - param['circle_radius'],
            center_y - param['circle_radius'],
            center_x + param['circle_radius'],
            center_y + param['circle_radius']
        ]
        param['small_circle_rect_question'].append(circle_rect)

    param['x_line_left_question'] = bigger_rect[0]
    param['x_line_right_question'] = bigger_rect[2]

    return param