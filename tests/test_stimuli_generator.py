import numpy as np
from utils.stimuli_generator import stimuli_generator_madm

def test_stimuli_generator_madm():
    num_attributes = 4
    num_trials = 10
    stimuli = stimuli_generator_madm(num_attributes, num_trials)
    assert len(stimuli) == num_trials
    weights = np.arange(num_attributes, 0, -1)
    for mat in stimuli:
        assert mat.shape == (num_attributes, 2)
        sum1 = np.dot(mat[:, 0], weights)
        sum2 = np.dot(mat[:, 1], weights)
        assert sum1 != sum2 