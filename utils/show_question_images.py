"""
Show question images
Converted from showQuestionImages.m
"""

from psychopy import visual
from utils.handle_fixation import handle_fixation
from draw_dashed_lines import draw_dashed_lines


def show_question_images(param):
    """
    Display question image pair with fixation control
    
    Parameters:
    -----------
    param : dict
        Experiment parameters
        
    Returns:
    --------
    param : dict
        Updated parameters with fixation data
    """
    # Draw initial fixation circles for questions
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
    
    param = draw_dashed_lines(param, param['white'], param['blue'])
    param['win'].flip()
    
    ## First question image
    param = handle_fixation(param, param['center_x_question'][0], 
                           param['center_y_question'][0], 0.3)
    
    # Prepare rectangles
    rect = param['img_rects_question'][0]
    param['bigger_rect_question1'] = [
        rect[0] - param['expand'],
        rect[1] - param['expand'],
        rect[2] + param['expand'],
        rect[3] + param['expand']
    ]
    
    # Helper function to draw background circle
    def draw_bg_circle(bigger_rect, color):
        x_psy = (bigger_rect[0] + bigger_rect[2]) / 2 - param['screen_x_pixels'] / 2
        y_psy = -((bigger_rect[1] + bigger_rect[3]) / 2 - param['screen_y_pixels'] / 2)
        width = bigger_rect[2] - bigger_rect[0]
        height = bigger_rect[3] - bigger_rect[1]
        
        circle = visual.Circle(
            param['win'],
            radius=max(width, height) / 2,
            pos=[x_psy, y_psy],
            fillColor=color,
            lineColor=color
        )
        circle.draw()
    
    # Draw backgrounds for all images
    draw_bg_circle(param['bigger_rect_question1'], param['grey'])
    draw_bg_circle(param['bigger_rect_ex1'], param['grey'])
    draw_bg_circle(param['bigger_rect_ex2'], param['grey'])
    
    # Draw all images
    param['img_textures_example'][0].draw()
    param['img_textures_example'][1].draw()
    param['img_textures_question'][0].draw()
    
    # Draw second question fixation circle
    rect = param['small_circle_rect_question'][1]
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
    
    param = draw_dashed_lines(param, param['white'], param['blue'])
    param['win'].flip()
    
    if param['occlude']:
        param['fixation_question1'] = {
            'fr_time': param['fr_time'],
            'eye_x': param['eye_x'],
            'eye_y': param['eye_y'],
            'pupil_size': param['pupil_size'],
            'frame_start': param['frame_start'],
            'frame_end': param['frame_end']
        }
    
    ## Second question image
    param = handle_fixation(param, param['center_x_question'][1], 
                           param['center_y_question'][1], 0.3)
    
    # Prepare second question rectangle
    rect = param['img_rects_question'][1]
    param['bigger_rect_question2'] = [
        rect[0] - param['expand'],
        rect[1] - param['expand'],
        rect[2] + param['expand'],
        rect[3] + param['expand']
    ]
    
    # Draw backgrounds for all images
    draw_bg_circle(param['bigger_rect_question1'], param['grey'])
    draw_bg_circle(param['bigger_rect_question2'], param['grey'])
    draw_bg_circle(param['bigger_rect_ex1'], param['grey'])
    draw_bg_circle(param['bigger_rect_ex2'], param['grey'])
    
    # Draw all images
    param['img_textures_question'][1].draw()
    param['img_textures_example'][0].draw()
    param['img_textures_example'][1].draw()
    param['img_textures_question'][0].draw()
    
    param = draw_dashed_lines(param, param['white'], param['white'])
    param['win'].flip()
    
    if param['occlude']:
        param['fixation_question2'] = {
            'fr_time': param['fr_time'],
            'eye_x': param['eye_x'],
            'eye_y': param['eye_y'],
            'pupil_size': param['pupil_size'],
            'frame_start': param['frame_start'],
            'frame_end': param['frame_end']
        }
    
    return param
