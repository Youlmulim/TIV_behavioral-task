"""
Attention check questions - mouse-click behavioral version.
"""

import random
from psychopy import visual, event, core


ATTENTION_QUESTIONS = [
    {
        'type': 'instruction',
        'question': 'To show you are paying attention, please select "Strongly Agree" below.',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'correct': 4,
    },
    {
        'type': 'instruction',
        'question': 'Please select "Blue" from the options below to confirm you are reading carefully.',
        'options': ['Red', 'Green', 'Blue', 'Yellow', 'Purple'],
        'correct': 2,
    },
    {
        'type': 'instruction',
        'question': 'This is an attention check. Please choose the third option.',
        'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'],
        'correct': 2,
    },
    {
        'type': 'instruction',
        'question': 'To confirm attention, select "Never" below.',
        'options': ['Always', 'Often', 'Sometimes', 'Rarely', 'Never'],
        'correct': 4,
    },
    {
        'type': 'instruction',
        'question': 'If you are reading this carefully, please choose "Cat" below.',
        'options': ['Dog', 'Bird', 'Cat', 'Fish', 'Horse'],
        'correct': 2,
    },
]


def get_random_check_sequence(num_to_select=6):
    """Return a shuffled list of attention-check dictionaries."""
    shuffled = ATTENTION_QUESTIONS.copy()
    random.shuffle(shuffled)
    return shuffled[:min(num_to_select, len(shuffled))]


def _draw_attention_screen(win, param, question_dict):
    question_text = visual.TextStim(
        win,
        text=question_dict['question'],
        pos=[0, 170],
        height=40,
        color=param['white'],
        wrapWidth=1200,
    )
    instr = visual.TextStim(
        win,
        text="Click one option to answer",
        pos=[0, -350],
        height=25,
        color=[0.7, 0.7, 0.7],
    )

    option_regions = []
    question_text.draw()
    instr.draw()

    for i, option in enumerate(question_dict['options']):
        y = 60 - i * 70
        rect = visual.Rect(
            win,
            width=760,
            height=52,
            pos=[0, y],
            fillColor=None,
            lineColor=param['white'],
            lineWidth=2,
        )
        label = visual.TextStim(
            win,
            text=f"{i + 1}. {option}",
            pos=[0, y],
            height=30,
            color=param['white'],
            wrapWidth=720,
        )
        rect.draw()
        label.draw()
        option_regions.append((i, -380, 380, y - 26, y + 26))

    win.flip()
    return option_regions


def _wait_with_escape(param, seconds):
    timer = core.Clock()
    while timer.getTime() < seconds:
        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            param['win'].close()
            core.quit()
        core.wait(0.01)


def show_single_attention_question(param, question_dict, current_idx, total_checks=6):
    """Display one attention question and return whether the click was correct."""
    win = param['win']
    mouse = event.Mouse(win=win)
    mouse.clickReset()

    while True:
        option_regions = _draw_attention_screen(win, param, question_dict)

        keys = event.getKeys(['escape'])
        if 'escape' in keys:
            win.close()
            core.quit()

        x, y = mouse.getPos()
        if mouse.getPressed()[0]:
            selected = None
            for idx, x_min, x_max, y_min, y_max in option_regions:
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    selected = idx
                    break

            while mouse.getPressed()[0]:
                keys = event.getKeys(['escape'])
                if 'escape' in keys:
                    win.close()
                    core.quit()
                core.wait(0.01)

            if selected is None:
                _wait_with_escape(param, 0.05)
                continue

            is_correct = selected == question_dict['correct']
            feedback_text = "✓ Correct!" if is_correct else "✗ Incorrect"
            feedback_color = [0, 1, 0] if is_correct else [1, 0, 0]
            feedback = visual.TextStim(
                win,
                text=feedback_text,
                pos=[0, 0],
                height=60,
                color=feedback_color,
            )
            feedback.draw()
            win.flip()
            _wait_with_escape(param, 1.0)
            return is_correct

        core.wait(0.01)
