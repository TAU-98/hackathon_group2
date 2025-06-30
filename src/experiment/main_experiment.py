import numpy as np
import pygame
import time
import json
from src.experiment.stimuli_generator import stimuli_generator_madm
from src.utils.visualization import (
    show_instruction_screen, show_candidate_table, show_feedback, show_score
)

# Mock eye-tracking integration
class EyeTracker:
    def __init__(self):
        self.events = []
    def start_recording(self):
        self.events.append(('start_recording', time.time()))
    def stop_recording(self):
        self.events.append(('stop_recording', time.time()))
    def send_message(self, msg):
        self.events.append((msg, time.time()))

def initialize_experiment():
    """
    Set up experiment parameters, load images, and initialize pygame.
    """
    pass

def run_trial(screen, font, mat, attributes, weights, text_color, bg_color, feedback_color, tracker, practice=False):
    show_candidate_table(screen, attributes, weights, mat[:, 0], mat[:, 1], font, text_color, bg_color)
    pygame.event.clear()
    start_time = time.time()
    response = None
    rt = None
    correct = None
    timeout = 4 if len(attributes) == 4 else 3
    # Compute correct answer
    sum_a = np.dot(mat[:, 0], weights)
    sum_b = np.dot(mat[:, 1], weights)
    if sum_a > sum_b:
        correct_ans = 'd'  # left
    else:
        correct_ans = 'k'  # right
    tracker.send_message('Stimulus ON')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in ['d', 'k']:
                    response = key
                    rt = time.time() - start_time
        if response is not None:
            tracker.send_message('Stimulus OFF')
            if response == 'd':
                tracker.send_message('RESPONSE LEFT')
            else:
                tracker.send_message('RESPONSE RIGHT')
            correct = (response == correct_ans)
            msg = 'Correct' if correct else 'Incorrect'
            show_feedback(screen, msg, font, feedback_color if not correct else text_color, bg_color)
            pygame.time.wait(800)
            break
        if time.time() - start_time > timeout:
            tracker.send_message('Stimulus OFF')
            show_feedback(screen, 'Too slow!', font, feedback_color, bg_color)
            pygame.time.wait(800)
            correct = False
            response = None
            rt = None
            break
    return {
        'attributes': attributes,
        'weights': weights,
        'values_a': mat[:, 0].tolist(),
        'values_b': mat[:, 1].tolist(),
        'response': response,
        'rt': rt,
        'correct': correct,
        'practice': practice
    }

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def run_experiment(num_sets=2, num_trials=10, num_practice=2, break_time=5):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('MADM Main Experiment (Eye-Tracking)')
    font = pygame.font.SysFont('Arial', 32)
    bg_color = (0, 0, 0)
    text_color = (255, 255, 0)
    feedback_color = (255, 0, 0)
    clock = pygame.time.Clock()
    results = []
    tracker = EyeTracker()
    attr_sets = [
        (['intelligence', 'work ethic', 'easy to work with'], [3, 2, 1]),
        (['intelligence', 'work ethic', 'easy to work with', 'creativity'], [4, 3, 2, 1])
    ]
    instructions = [
        "Welcome to the experiment!\nPress any key to continue.",
        "You will see pairs of candidates.\nChoose the better one using D (left) or K (right).\nPress any key to start practice."
    ]
    for text in instructions:
        show_instruction_screen(screen, text, font, text_color, bg_color)
        wait_for_key()
    for set_idx in range(num_sets):
        attributes, weights = attr_sets[set_idx]
        tracker.start_recording()
        tracker.send_message(f'START BLOCK {set_idx+1}')
        # Practice
        show_instruction_screen(screen, f"Practice: {len(attributes)} attributes\nPress any key to start.", font, text_color, bg_color)
        wait_for_key()
        practice_stimuli = stimuli_generator_madm(len(attributes), num_practice)
        for mat in practice_stimuli:
            run_trial(screen, font, mat, attributes, weights, text_color, bg_color, feedback_color, tracker, practice=True)
        show_instruction_screen(screen, "Practice complete!\nPress any key to continue.", font, text_color, bg_color)
        wait_for_key()
        # Main trials
        show_instruction_screen(screen, f"Main trials: {len(attributes)} attributes\nPress any key to start.", font, text_color, bg_color)
        wait_for_key()
        stimuli = stimuli_generator_madm(len(attributes), num_trials)
        for i, mat in enumerate(stimuli):
            tracker.send_message(f'TRIAL {i+1} SET {set_idx+1}')
            res = run_trial(screen, font, mat, attributes, weights, text_color, bg_color, feedback_color, tracker, practice=False)
            results.append(res)
            if (i + 1) % break_time == 0 and (i + 1) != num_trials:
                show_instruction_screen(screen, "Break!\nPress any key to continue.", font, text_color, bg_color)
                wait_for_key()
        tracker.stop_recording()
        tracker.send_message('END BLOCK')
    # Save results
    save_results({'results': results, 'eye_tracking': tracker.events}, 'main_experiment_results.json')
    show_instruction_screen(screen, "Experiment complete!\nThank you!", font, text_color, bg_color)
    pygame.time.wait(2000)
    pygame.quit()

def save_results(data, filename):
    """
    Save experiment results to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    run_experiment() 