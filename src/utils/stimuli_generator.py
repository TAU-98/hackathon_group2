import numpy as np

def stimuli_generator_madm(num_attributes, num_trials):
    """
    Generate a list of matrices for the MADM experiment.
    Each matrix is of shape (num_attributes, 2), with random integers 1-9.
    Ensures that the weighted sum of the two alternatives is not equal.
    """
    stimuli = []
    weights = np.arange(num_attributes, 0, -1)
    for _ in range(num_trials):
        mat = np.random.randint(1, 10, size=(num_attributes, 2))
        # Ensure alternatives have different weighted sums
        while np.dot(mat[:, 0], weights) == np.dot(mat[:, 1], weights):
            mat = np.random.randint(1, 10, size=(num_attributes, 2))
        stimuli.append(mat)
    return stimuli 