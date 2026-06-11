"""
Show example images
Converted from showExampleImages.m
"""

from psychopy import visual
from utils.handle_fixation import handle_fixation
from draw_dashed_lines import draw_dashed_lines


def show_example_images(param):
    """
    Display example image pair with fixation control
    
    Parameters:
    -----------
    param : dict
        Experiment parameters
        
    Returns:
    --------
    param : dict
        Updated parameters with fixation data
    """
    # Draw initial fixation circles
    for i in range(2):
        rect = param['small_circle_rect_example'][i]
        x_psy = (rect[0] + rect[2]) / 2 - param['screen_x_pixels'] / 2
        y_psy = -((rect[1] + rect[3]) / 2 - param['screen_y_pixels'] / 2)
        
        circle = visual.Circle(
            param['win'],
            radius=param['circle_radius'],
            pos=[x_psy, y_psy],
            fillColor=param['blue'],
            lineColor=param['blue']
        )
        circle.draw()
        
        rect = param['small_circle_rect_question'][i]
        x_psy = (rect[0] + rect[2]) / 2 - param['screen_x_pixels'] / 2
        y_psy = -((rect[1] + rect[3]) / 2 - param['screen_y_pixels'] / 2)
        
        circle = visual.Circle(
            param['win'],
            radius=param['circle_radius'],
            pos=[x_psy, y_psy],
            fillColor=param['blue'],
            lineColor=param['blue']
        )
        circle.draw()
    
    param = draw_dashed_lines(param, param['blue'], param['white'])
    param['win'].flip()
    
    ## First image
    param = handle_fixation(param, param['center_x_example'][0], 
                           param['center_y_example'][0], 0.3)
    
    # Draw background circle and first example image
    rect = param['img_rects_example'][0]
    param['bigger_rect_ex1'] = [
        rect[0] - param['expand'],
        rect[1] - param['expand'],
        rect[2] + param['expand'],
        rect[3] + param['expand']
    ]
    
    # Draw grey background circle
    x_psy = (param['bigger_rect_ex1'][0] + param['bigger_rect_ex1'][2]) / 2 - param['screen_x_pixels'] / 2
    y_psy = -((param['bigger_rect_ex1'][1] + param['bigger_rect_ex1'][3]) / 2 - param['screen_y_pixels'] / 2)
    width = param['bigger_rect_ex1'][2] - param['bigger_rect_ex1'][0]
    height = param['bigger_rect_ex1'][3] - param['bigger_rect_ex1'][1]
    
    bg_circle = visual.Circle(
        param['win'],
        radius=max(width, height) / 2,
        pos=[x_psy, y_psy],
        fillColor=param['grey'],
        lineColor=param['grey']
    )
    bg_circle.draw()
    
    # Draw first example image
    param['img_textures_example'][0].draw()
    
    # Draw second fixation circle
    rect = param['small_circle_rect_example'][1]
    x_psy = (rect[0] + rect[2]) / 2 - param['screen_x_pixels'] / 2
    y_psy = -((rect[1] + rect[3]) / 2 - param['screen_y_pixels'] / 2)
    
    circle = visual.Circle(
        param['win'],
        radius=param['circle_radius'],
        pos=[x_psy, y_psy],
        fillColor=param['blue'],
        lineColor=param['blue']
    )
    circle.draw()
    
    # Draw question fixation circles
    for i in range(2):
        rect = param['small_circle_rect_question'][i]
        x_psy = (rect[0] + rect[2]) / 2 - param['screen_x_pixels'] / 2
        y_psy = -((rect[1] + rect[3]) / 2 - param['screen_y_pixels'] / 2)
        
        circle = visual.Circle(
            param['win'],
            radius=param['circle_radius'],
            pos=[x_psy, y_psy],
            fillColor=param['blue'],
            lineColor=param['blue']
        )
        circle.draw()
    
    param = draw_dashed_lines(param, param['blue'], param['white'])
    param['win'].flip()
    
    if param['occlude']:
        param['fixation_example1'] = {
            'fr_time': param['fr_time'],
            'eye_x': param['eye_x'],
            'eye_y': param['eye_y'],
            'pupil_size': param['pupil_size'],
            'frame_start': param['frame_start'],
            'frame_end': param['frame_end']
        }
    
    ## Second image
    param = handle_fixation(param, param['center_x_example'][1], 
                           param['center_y_example'][1], 0.3)
    
    # Draw both example images with backgrounds
    rect = param['img_rects_example'][1]
    param['bigger_rect_ex2'] = [
        rect[0] - param['expand'],
        rect[1] ,
        rect[2] + param['expand'],
        rect[3] + param['expand']
    ]
    
    # Draw first image background and image
    bg_circle.draw()
    param['img_textures_example'][0].draw()
    
    # Draw second image background
    x_psy = (param['bigger_rect_ex2'][0] + param['bigger_rect_ex2'][2]) / 2 - param['screen_x_pixels'] / 2
    y_psy = -((param['bigger_rect_ex2'][1] + param['bigger_rect_ex2'][3]) / 2 - param['screen_y_pixels'] / 2)
    width = param['bigger_rect_ex2'][2] - param['bigger_rect_ex2'][0]
    height = param['bigger_rect_ex2'][3] - param['bigger_rect_ex2'][1]
    
    bg_circle2 = visual.Circle(
        param['win'],
        radius=max(width, height) / 2,
        pos=[x_psy, y_psy],
        fillColor=param['grey'],
        lineColor=param['grey']
    )
    bg_circle2.draw()
    
    # Draw second example image
    param['img_textures_example'][1].draw()
    
    param = draw_dashed_lines(param, param['blue'], param['white'])
    
    if param['occlude']:
        param['fixation_example2'] = {
            'fr_time': param['fr_time'],
            'eye_x': param['eye_x'],
            'eye_y': param['eye_y'],
            'pupil_size': param['pupil_size'],
            'frame_start': param['frame_start'],
            'frame_end': param['frame_end']
        }
    
    return param
