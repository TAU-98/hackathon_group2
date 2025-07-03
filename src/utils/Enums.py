import pygame

class Colors:
    BG_COLOR = (10, 10, 20)
    TEXT_COLOR = (255, 255, 0)
    FEEDBACK_COLOR = (255, 0, 0)
    ACCENT_COLOR = (0, 200, 255)

class Consts:
    FIELDS = ['Name', 'Age', 'Gender']
    SAVED_FILE_NAME = 'main_experiment_results.json'
    ATTRIBUTES_SETS = [
        (['intelligence', 'work ethic', 'sociable'], [3, 2, 1]),
        (['intelligence', 'work ethic', 'sociable', 'creativity'], [4, 3, 2, 1])
    ]