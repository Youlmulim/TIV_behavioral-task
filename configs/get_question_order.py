"""
Get question order and image pairs
Converted from getQuestionOrder.m
"""

import numpy as np


def get_question_order(question_matrix, question_num):
    """
    Get image pairs for a specific question
    
    Parameters:
    -----------
    question_matrix : numpy.ndarray
        Matrix of question combinations
    question_num : int
        Question number (0-indexed)
        
    Returns:
    --------
    image_pairs : list
        List of image pair tuples
        
    Example:
    --------
    >>> matrix = np.array([['AD', 'DA', 'AB'], ['BA', 'AC', 'CA']], dtype=object)
    >>> pairs = get_question_order(matrix, 0)
    >>> # Returns: [('a_1', 'd_1'), ('d_1', 'a_1'), ('a_1', 'b_1')]
    """
    # Define image pairs
    a = ["a_1", "a_2"]
    b = ["b_1", "b_2"]
    c = ["c_1", "c_2"]
    d = ["d_1", "d_2"]
    
    # List of all image sets
    sets = [a, b, c, d]
    
    # Create mapping from letters to indices
    letter_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    # Get question combinations
    question = question_matrix[question_num, :]
    image_pairs = []
    
    for combo in question:
        # Handle different possible data types from .mat file
        if hasattr(combo, 'item'):
            combo_str = combo.item()
        else:
            combo_str = str(combo)
        
        # Get indices for the pairs
        idx1 = letter_map[combo_str[0]]
        idx2 = letter_map[combo_str[1]]
        
        # Create image pair
        image_pairs.append((sets[idx1][0], sets[idx2][0]))
    
    return image_pairs
