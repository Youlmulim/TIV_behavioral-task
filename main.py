"""
Main experiment script - behavioral mouse-click version.

Data saving is intentionally minimal:
    - trial/phase identifiers needed to align responses with the task
    - selected rating
    - reaction time

Eye-tracking, pupil, gaze, and mouse-trajectory data are not recorded.
"""

import os
import sys
import random
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from psychopy import visual, core, event

# Add the configs and utils directories to path
sys.path.insert(0, str(Path(__file__).parent / 'configs'))
sys.path.insert(0, str(Path(__file__).parent / 'utils'))

# Import custom modules
from configs.initiate_params import initiate_params
from utils.waiting_screen import waiting_screen
from configs.get_question_order import get_question_order
from utils.ask_question import ask_question
from utils.attention_checks import (
    ATTENTION_QUESTIONS,
    get_random_check_sequence,
    show_single_attention_question,
)

def save_data_csv(param, timestamp):
    """Save only behavioral rating and reaction-time data."""
    df = pd.DataFrame(param['data'], columns=param['headers'])
    csv_path = param['save_dir'] / f"{timestamp}_behavior.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


def terminate_experiment(param, reason):
    """Show termination screen and quit for failed attention checks."""
    msg = visual.TextStim(
        param['win'],
        text=f"Experiment Terminated\n\nReason: {reason}\n",
        color='red',
        height=30,
        wrapWidth=1000,
    )
    msg.draw()
    param['win'].flip()
    core.wait(5)
    param['win'].close()
    core.quit()


def main(subject, eye_tracking=False):
    """
    Run the behavioral experiment.

    The eye_tracking argument is kept for backward compatibility with older
    command-line calls, but this version always runs as mouse-click-only.
    """
    param = initiate_params(subject, eye_tracking=False)
    d = datetime.now()
    timestamp_str = d.strftime("%H-%M")

    # --- SETUP ATTENTION CHECKS ---
    num_checks = min(6, len(ATTENTION_QUESTIONS))
    attn_pool = get_random_check_sequence(num_checks)
    total_questions = len(param['question_matrix'])

    # Select random indices to insert checks, spread out with no back-to-back checks.
    check_slots = []
    possible_indices = list(range(1, total_questions + 1))
    while len(check_slots) < num_checks and possible_indices:
        idx = random.choice(possible_indices)
        check_slots.append(idx)
        for n in [idx - 1, idx, idx + 1]:
            if n in possible_indices:
                possible_indices.remove(n)
    check_slots = set(check_slots)

    attn_results = []
    # ------------------------------

    param['trial_counter'] = 1
    param = waiting_screen(param, first_start=True)

    # Main experiment loop
    for question_id in param["question_ids"]:
        param["question_num"] = question_id

        param["randomized_question_pairs"] = get_question_order(
            param["question_matrix"],
            question_id - 1
        )

        for subtrial in range(param["question_matrix"].shape[1]):
            param["sub_trial"] = subtrial

            param = ask_question(param)
            param["trial_counter"] += 1

            save_data_csv(param, timestamp_str)

        # --- RUN ATTENTION CHECK ---
        if question_id in check_slots and len(attn_results) < num_checks:
            current_attn_idx = len(attn_results)
            is_correct = show_single_attention_question(
                param, attn_pool[current_attn_idx], current_attn_idx + 1, num_checks
            )
            attn_results.append(is_correct)

            # Consecutive Failure Rule: terminate after 3 wrong checks in a row.
            if len(attn_results) >= 3:
                if (not attn_results[-1] and
                        not attn_results[-2] and
                        not attn_results[-3]):
                    terminate_experiment(
                        param,
                        "Experiment ended due to three consecutive failed attention checks.",
                    )

    param['save_dir'].mkdir(parents=True, exist_ok=True)
    final_csv = save_data_csv(param, f"{timestamp_str}_FINAL")

    print(f"Experiment Complete. Attention Score: {attn_results.count(True)}/{num_checks}")
    print(f"Behavioral data saved to: {final_csv}")
    param['win'].close()
    core.quit()


if __name__ == "__main__":
    subject_id = sys.argv[1] if len(sys.argv) > 1 else 'test_subject'
    # Any second argument is ignored in this behavior-only version.
    main(subject_id, eye_tracking=False)
