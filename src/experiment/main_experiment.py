import numpy as np
import pygame
import time
import json
from utils.stimuli_generator import stimuli_generator_madm
from src.utils.visualization import Visualization
from src.experiment.Enums import Colors, Consts

# Mock eye-tracking integration
class EyeTracker:
    def __init__(self, use: bool):
        self.events = []
        self.use = use
    def start_recording(self):
        if self.use:
            self.events.append(('start_recording', time.time()))
    def stop_recording(self):
        if self.use:
            self.events.append(('stop_recording', time.time()))
    def send_message(self, msg):
        if self.use:
            self.events.append((msg, time.time()))

class MainExperiment:
    """the class run the experiment.
    Input:
        use_eye_tracker: if true will create a timeline for the eyetracker with events
        num_sets: numbers of different sets in the experiment
        num_trials: number of trials in each set
        num_practice: number of trials for practice
        break_time: how much trials before a break"""
    def __init__(self, use_eye_tracker=True, num_sets=2, num_trials=10, num_practice=2, break_time=5):
        self.num_sets = num_sets
        self.num_trials = num_trials
        self.num_practice = num_practice
        self.break_time = break_time
        self.results = []
        self.use_eye_tracker = use_eye_tracker
        self.tracker = EyeTracker(use= self.use_eye_tracker)

        pygame.init()
        screen = pygame.display.set_mode((1000, 700))
        font = pygame.font.SysFont('Arial Rounded MT Bold', 32)
        self.visualization = Visualization(screen=screen, font=font, accent_color=Colors.ACCENT_COLOR,
                                           bg_color=Colors.BG_COLOR, text_color=Colors.TEXT_COLOR)

    def run_trial(self, mat, attributes, weights, text_color, feedback_color, title, practice=False):
        """the function run each trial of the experiment.
        the function get the attributes, the matrix and the weights and:
        1. show the attributes in the screen.
        2. calculate the correct answer.
        3. read the user input and return dict with the data of the trial
        ** the function update the tracker when needed"""
        self.visualization.show_candidate_table(attributes=attributes, weights=weights, values_a=mat[:, 0],
                                                values_b=mat[:, 1], title=title)
        pygame.event.clear()
        start_time = time.time()
        response = None
        rt = None
        timeout = len(attributes)
        correct_ans = self._compute_correct_answer(mat=mat, weights=weights)
        self.tracker.send_message('Stimulus ON')
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
                self.tracker.send_message('Stimulus OFF')
                if response == 'd':
                    self.tracker.send_message('RESPONSE LEFT')
                else:
                    self.tracker.send_message('RESPONSE RIGHT')
                correct = (response == correct_ans)
                msg = 'Correct' if correct else 'Incorrect'
                self.visualization.show_feedback(message=msg, color=feedback_color if not correct else text_color, title='Feedback')
                pygame.time.wait(800)
                break
            if time.time() - start_time > timeout:
                self.tracker.send_message('Stimulus OFF')
                self.visualization.show_feedback(message='Too slow!', color=feedback_color, title='Feedback')
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
    def _compute_correct_answer(mat, weights) -> str:
        """the function calculate the correct answer"""
        sum_a = np.dot(mat[:, 0], weights)
        sum_b = np.dot(mat[:, 1], weights)
        if sum_a > sum_b:
            return 'd'  # left
        else:
            return 'k'  # right

    @staticmethod
    def wait_for_key():
        """the function is wait for input from user"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run_experiment(self):
        """the main function of the game. the function:
        1. set the pygame object
        2. show the demographics form and let the subject to fill the form
        3. show the subject the instruction
        4. in each set of attributes:
            a. create practice for subject
            b. create real task for subject
            ** start and stop the track recorder and send message to it
        5. save the results"""
        pygame.init()
        pygame.display.set_caption('MADM Main Experiment (Eye-Tracking)')

        demographics = self.visualization.show_demographics_form()

        instructions = ["Welcome to the experiment!\nPress any key to continue.",
                        "You will see pairs of candidates.\nChoose the better one using D (left) or K (right).\n"
                        "Press any key to start practice."]
        for text in instructions:
            self.visualization.show_instruction_screen(text=text, title='Instructions')
            self.wait_for_key()

        for set_idx in range(self.num_sets):
            attributes, weights = Consts.ATTRIBUTES_SETS[set_idx]
            self.tracker.start_recording()
            self.tracker.send_message(f'START BLOCK {set_idx+1}')

            self._run_practice(attributes=attributes, weights=weights)
            self._run_main_part(attributes=attributes, set_idx=set_idx, weights=weights)

            self.tracker.stop_recording()
            self.tracker.send_message('END BLOCK')

        tracker_record = self.tracker.events if self.use_eye_tracker else "not record"
        self.save_results({'demographics': demographics, 'results': self.results,
                               'eye_tracking': tracker_record}, Consts.SAVED_FILE_NAME)

        self.visualization.show_instruction_screen(text= "Experiment complete!\nThank you!", title='End',)
        pygame.time.wait(2000)
        pygame.quit()

    def _run_practice(self, attributes, weights):
        """this function is run the practice part of the experiment
        1. show the instruction
        2. generate the matrix
        3. run in loop each trial of the practice"""
        self.visualization.show_instruction_screen(text= f"Practice: {len(attributes)} attributes\nPress any key to start.",
                                                   title='Practice')
        self.wait_for_key()
        practice_stimuli = stimuli_generator_madm(len(attributes), self.num_practice)
        for mat in practice_stimuli:
            self.run_trial(mat=mat, attributes=attributes, weights=weights, text_color=Colors.TEXT_COLOR,
                           feedback_color=Colors.FEEDBACK_COLOR, title='Practice Trial', practice=True)

        self.visualization.show_instruction_screen(text= "Practice complete!\nPress any key to continue.",
                                                   title='Practice')
        self.wait_for_key()

    def _run_main_part(self, attributes, set_idx, weights):
        """this function is run the practice part of the experiment
        1. show the instruction
        2. generate the matrix
        3. run in loop each trial of the experiment
        4. save the data in results"""
        self.visualization.show_instruction_screen(text=f"Main trials: {len(attributes)} attributes\nPress any key to start.",
                                                   title='Main Trials')
        self.wait_for_key()
        stimuli = stimuli_generator_madm(len(attributes), self.num_trials)
        for i, mat in enumerate(stimuli):
            self.tracker.send_message(f'TRIAL {i + 1} SET {set_idx + 1}')
            res = self.run_trial(mat=mat, attributes=attributes, weights=weights, text_color=Colors.TEXT_COLOR,
                                 feedback_color=Colors.FEEDBACK_COLOR, title='Trial', practice=False)
            self.results.append(res)
            if (i + 1) % self.break_time == 0 and (i + 1) != self.num_trials:
                self.visualization.show_instruction_screen(text= "Break!\nPress any key to continue.", title='Break')
                self.wait_for_key()

    @staticmethod
    def save_results(data:dict, filename:str):
        """
        Save experiment results to a JSON file.
        """
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == '__main__':
    exp = MainExperiment()
    exp.run_experiment()