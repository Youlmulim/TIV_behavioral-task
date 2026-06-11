"""
Load matrices and define experiment parameters
Converted from getParamDetails.m
"""

import numpy as np
import scipy.io as sio
from pathlib import Path


def get_param_details(param):
    """
    Load experiment matrices and define parameters

    Parameters:
    -----------
    param : dict
        Existing parameter dictionary

    Returns:
    --------
    param : dict
        Updated parameter dictionary
    """
    # Get the directory where this script is located (configs/)
    script_dir = Path(__file__).parent

    # Load matrices from configs folder
    left_right_matrix = sio.loadmat(script_dir / 'leftRightMatrix.mat')['binaryMatrix']
    question_matrix = sio.loadmat(script_dir / 'questionMatrix.mat')['questionMatrix']
    scoring_order = sio.loadmat(script_dir / 'scoringOrder.mat')['shuffledData']

    # Randomize order
    left_right_perm = np.random.permutation(left_right_matrix.shape[0])
    scoring_perm = np.random.permutation(scoring_order.shape[1])

    param['question_matrix'] = question_matrix
    param['left_right_matrix'] = left_right_matrix[left_right_perm, :]
    param['scoring_order'] = scoring_order[0, scoring_perm]

    # Define colors (normalized to [-1, 1] for PsychoPy)
    param['white'] = [1, 1, 1]
    param['black'] = [-1, -1, -1]
    param['grey'] = [0, 0, 0]
    param['red'] = [1, -1, -1]
    param['green'] = [-1, 1, -1]
    param['blue'] = [-1, -1, 1]
    param['yellow'] = [1, 1, -1]
    param['orange'] = [1, 0.1, -0.5]
    param['purple'] = [1, -1, 1]
    param['salmon'] = [0.96, 0.0, -0.1]

    # OPTIMIZED: Larger images, better proportions
    # Rectangle definitions (in pixels) - optimized for 1710x1112 screen
    param['base_rect'] = [0, 0, 180, 180]    # Increased from 150
    param['out_rect'] = [0, 0, 320, 260]     # Increased from 250x200
    param['b_rect_one'] = [0, 0, 50, 180]
    param['b_rect_two'] = [0, 0, 180, 50]
    param['small_circle'] = [0, 0, 120, 120]

    # Calculate centers
    param['x_center_small'] = param['out_rect'][2]
    param['y_center_small'] = param['out_rect'][3]

    # Rectangle for showing stimuli - Better sizing
    rect_width = int(param['out_rect'][2] * 1.3)   # Slightly larger
    rect_height = int(param['out_rect'][3] * 1.3)
    param['rect_zero'] = [
        param['screen_x_pixels'] * 0.5 - rect_width / 2,
        param['screen_y_pixels'] * 0.25 - rect_height / 2,
        param['screen_x_pixels'] * 0.5 + rect_width / 2,
        param['screen_y_pixels'] * 0.25 + rect_height / 2
    ]

    # Grid parameters
    num_rows = 4
    num_cols = 4
    param['sub_rect_width'] = (param['rect_zero'][2] - param['rect_zero'][0]) / num_cols
    param['sub_rect_height'] = (param['rect_zero'][3] - param['rect_zero'][1]) / num_rows

    # Image and scoring parameters - OPTIMIZED
    param['expand'] = 35  # Slightly larger expand
    param['circle_radius'] = 18  # Slightly larger fixation circles
    param['num_buttons'] = 7
    param['center_x'] = param['screen_x_pixels'] / 2
    param['center_y'] = param['screen_y_pixels'] / 2

    # Scoring circles - keep reasonable size
    max_radius = min(param['screen_x_pixels'], param['screen_y_pixels']) * 0.32
    param['big_radius'] = min(380, max_radius)  # Slightly smaller for better fit
    param['small_radius'] = 45

    # Display parameters
    param['frame_size'] = 6
    param['frame_color'] = param['black']
    param['screen_color'] = param['grey']
    param['fixation_threshold'] = 1.0  # 1 second

    # Position ratios
    param['ratio_x_show'] = [0.5, 0.5]
    param['ratio_x_ask'] = [0.5, 0.25, 0.75]
    param['ratio_y_show'] = [0.25, 0.75]
    param['ratio_y_ask'] = [0.25, 0.75, 0.75]

    # Keyboard settings
    param['escape_key'] = 'escape'
    param['space_key'] = 'space'

    print(f"✓ Screen size: {param['screen_x_pixels']}x{param['screen_y_pixels']}")
    print(f"✓ Image size: {param['sub_rect_width']:.1f}x{param['sub_rect_height']:.1f}")
    print(f"✓ Scoring radius: {param['big_radius']:.1f}")

    return param