"""
Initialize experiment parameters - behavioral mouse-click version.
"""

from pathlib import Path
import numpy as np
from get_screen_details import get_screen_details
from get_param_details import get_param_details


def initiate_params(subject, eye_tracking=False):
    """
    Initialize experiment parameters.

    This behavior-only version does not initialize or record eye-tracking data.
    The eye_tracking argument is retained for backward compatibility and ignored.
    """
    param = get_screen_details()
    param = get_param_details(param)

    # Minimal behavioral output.
    # Phase = question number; Subtrial = within-phase rating trial.
    param['headers'] = [
        'Trial',
        'Question_Num',
        'Subtrial',
        'Rating',
        'Reaction_Time',
    ]

    # Force mouse-click-only behavior.
    param['occlude'] = False
    param['move_speed'] = 35

    # 실제로 존재하는 questions/questionN 폴더만 사용
    questions_dir = Path("questions")

    question_ids = []
    for q_dir in questions_dir.glob("question*"):
        if q_dir.is_dir():
            q_name = q_dir.name  # 예: "question3"

            if q_name.startswith("question"):
                q_num_str = q_name.replace("question", "")

                if q_num_str.isdigit():
                    question_ids.append(int(q_num_str))

    # 번호 순서 정렬
    question_ids = sorted(question_ids)

    # 참가자마다 제시 순서는 랜덤화
    question_ids = question_ids.copy()
    np.random.shuffle(question_ids)

    param["question_ids"] = question_ids
    param["n_questions"] = len(question_ids)

    # Data saving
    from datetime import date
    param['save_dir'] = Path.cwd() / "data" / subject / date.today().strftime("%Y-%m-%d")
    param['data'] = []
    param['save_dir'].mkdir(parents=True, exist_ok=True)

    return param
