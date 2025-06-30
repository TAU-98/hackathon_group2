import json
from src.experiment.main_experiment import save_results

def test_save_results(tmp_path):
    data = {'trial': [1, 2, 3], 'result': [True, False, True]}
    file_path = tmp_path / 'results.json'
    save_results(data, file_path)
    with open(file_path, 'r') as f:
        loaded = json.load(f)
    assert loaded == data 