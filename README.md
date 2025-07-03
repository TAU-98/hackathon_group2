# Eye-scan Monitoring of Decision Strategies in Multi-Attribute Choice

## Overview
This project is a Python-based implementation of a multi-attribute decision-making (MADM) experiment, originally developed in MATLAB. The experiment presents participants with pairs of job candidates, each described by several attributes, and asks them to make decisions under time pressure. The system is designed to integrate with eye-tracking hardware (mocked in this version) and supports dynamic visualization, trial customization, and real-time data collection for cognitive research.

## Features
- Replicates the original MATLAB experiment logic in Python
- Modular code for experiment logic, stimuli generation, and demographics
- (Mock) eye-tracking integration for future extensibility
- GUI-ready (using pygame, to be implemented)
- Unit tests for all core modules
- Easy data export in JSON format

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd hackathon
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- To run the main experiment (with eye-tracking mocked):
  ```python
  from src.experiment.main_experiment import run_experiment
  run_experiment()
  ```
- To run the MADM skewed experiment (no eye-tracking):
  ```python
  from src.experiment.madm_skewde import run_madm_skewde_experiment
  run_madm_skewde_experiment()
  ```
- To generate stimuli:
  ```python
  from src.experiment.stimuli_generator import stimuli_generator_madm
  stimuli = stimuli_generator_madm(num_attributes=4, num_trials=10)
  ```
- To collect demographics:
  ```python
  from src.experiment.demographics import collect_demographics, save_demographics
  demo = collect_demographics()
  save_demographics(demo, 'demographics.json')
  ```

## Testing
Run all tests using pytest:
```bash
pytest tests/
```

## Project Structure
```
hackathon/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── experiment/
│   │   ├── main_experiment.py
│   │   ├── madm_skewde.py
│   │   ├── demographics.py
│   │   └── stimuli_generator.py
│   └── utils/
│       └── visualization.py
├── tests/
│   ├── test_main_experiment.py
│   ├── test_madm_skewde.py
│   ├── test_demographics.py
│   └── test_stimuli_generator.py
└── assets/
    └── images/
```

## Notes
- The GUI and eye-tracking integration are currently mocked or in skeleton form. See code comments for extension points.
- For full experiment visuals, see the provided images in the assets/images directory.

---
For questions or contributions, please contact the project maintainer. 