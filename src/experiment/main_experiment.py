import numpy as np
import pygame
import time
import json
from src.experiment.stimuli_generator import stimuli_generator_madm
from src.utils.visualization import Visualization
from src.experiment.Enums import Colors, Consts

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

class MainExperiment:
    def __init__(self, num_sets=2, num_trials=10, num_practice=2, break_time=5):
        self.num_sets = num_sets
        self.num_trials = num_trials
        self.num_practice = num_practice
        self.break_time = break_time
        self.visualization = Visualization()
        self.tracker = EyeTracker()
        self.results = []

    def run_trial(self,screen, font, mat, attributes, weights, text_color, bg_color, feedback_color, tracker, accent_color, title, practice=False):
        self.visualization.show_candidate_table(screen, attributes, weights, mat[:, 0], mat[:, 1], font, text_color,
                                                bg_color, title=title, accent_color=accent_color)
        pygame.event.clear()
        start_time = time.time()
        response = None
        rt = None
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
                self.visualization.show_feedback(screen, msg, font, feedback_color if not correct else text_color, bg_color, title='Feedback', accent_color=accent_color)
                pygame.time.wait(800)
                break
            if time.time() - start_time > timeout:
                tracker.send_message('Stimulus OFF')
                self.visualization.show_feedback(screen, 'Too slow!', font, feedback_color, bg_color, title='Feedback', accent_color=accent_color)
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

    @staticmethod
    def wait_for_key():
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run_experiment(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption('MADM Main Experiment (Eye-Tracking)')
        font = pygame.font.SysFont('Arial Rounded MT Bold', 32)

        demographics = self.visualization.show_demographics_form(screen, font, Colors.BG_COLOR, Colors.ACCENT_COLOR)
        instructions = [
            "Welcome to the experiment!\nPress any key to continue.",
            "You will see pairs of candidates.\nChoose the better one using D (left) or K (right).\nPress any key to start practice."
        ]
        for text in instructions:
            self.visualization.show_instruction_screen(screen, text, font, Colors.TEXT_COLOR, Colors.BG_COLOR,
                                                       title='Instructions', accent_color=Colors.ACCENT_COLOR)
            self.wait_for_key()

        for set_idx in range(self.num_sets):
            attributes, weights = Consts.ATTRIBUTES_SETS[set_idx]
            self.tracker.start_recording()
            self.tracker.send_message(f'START BLOCK {set_idx+1}')
            self._run_practice(screen=screen, font=font, attributes=attributes, weights=weights)
            self._run_main_part(screen=screen, font=font, attributes=attributes, set_idx=set_idx, weights=weights)
            self.tracker.stop_recording()
            self.tracker.send_message('END BLOCK')
        # Save results

        self.save_results({'demographics': demographics, 'results': self.results, 'eye_tracking': self.tracker.events}, Consts.SAVED_FILE_NAME)
        self.visualization.show_instruction_screen(screen, "Experiment complete!\nThank you!", font,
                                                   Colors.TEXT_COLOR, Colors.BG_COLOR, title='End',
                                                   accent_color=Colors.ACCENT_COLOR)
        pygame.time.wait(2000)
        pygame.quit()

    def _run_practice(self, screen, font, attributes, weights):
        """this function is run the practice part of the experiment"""
        self.visualization.show_instruction_screen(screen,
                                                   f"Practice: {len(attributes)} attributes\nPress any key to start.",
                                                   font, Colors.TEXT_COLOR, Colors.BG_COLOR, title='Practice',
                                                   accent_color=Colors.ACCENT_COLOR)
        self.wait_for_key()
        practice_stimuli = stimuli_generator_madm(len(attributes), self.num_practice)
        for mat in practice_stimuli:
            self.run_trial(screen, font, mat, attributes, weights, Colors.TEXT_COLOR, Colors.BG_COLOR,
                           Colors.FEEDBACK_COLOR, self.tracker, Colors.ACCENT_COLOR, title='Practice Trial',
                           practice=True)

        self.visualization.show_instruction_screen(screen, "Practice complete!\nPress any key to continue.",
                                                   font, Colors.TEXT_COLOR, Colors.BG_COLOR, title='Practice',
                                                   accent_color=Colors.ACCENT_COLOR)
        self.wait_for_key()

    def _run_main_part(self, screen, font, attributes, set_idx, weights):
        """the function run the main part of the experiment. it runs the actual stage that we will save the data"""
        self.visualization.show_instruction_screen(screen,
                                                   f"Main trials: {len(attributes)} attributes\nPress any key to start.",
                                                   font, Colors.TEXT_COLOR, Colors.BG_COLOR, title='Main Trials',
                                                   accent_color=Colors.ACCENT_COLOR)
        self.wait_for_key()
        stimuli = stimuli_generator_madm(len(attributes), self.num_trials)
        for i, mat in enumerate(stimuli):
            self.tracker.send_message(f'TRIAL {i + 1} SET {set_idx + 1}')
            res = self.run_trial(screen, font, mat, attributes, weights, Colors.TEXT_COLOR, Colors.BG_COLOR,
                                 Colors.FEEDBACK_COLOR, self.tracker, Colors.ACCENT_COLOR, title='Trial',
                                 practice=False)
            self.results.append(res)
            if (i + 1) % self.break_time == 0 and (i + 1) != self.num_trials:
                self.visualization.show_instruction_screen(screen, "Break!\nPress any key to continue.", font,
                                                           Colors.TEXT_COLOR, Colors.BG_COLOR, title='Break',
                                                           accent_color=Colors.ACCENT_COLOR)
                self.wait_for_key()

    @staticmethod
    def save_results(data, filename):
        """
        Save experiment results to a JSON file.
        """
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == '__main__':
    exp = MainExperiment()
    exp.run_experiment()