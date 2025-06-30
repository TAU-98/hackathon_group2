import os
import json
from src.experiment.demographics import save_demographics

def test_save_demographics(tmp_path):
    demographics = {'name': 'Alice', 'age': '30', 'gender': 'Female'}
    file_path = tmp_path / 'demo.json'
    save_demographics(demographics, file_path)
    with open(file_path, 'r') as f:
        loaded = json.load(f)
    assert loaded == demographics

def test_collect_demographics(monkeypatch):
    from src.experiment.demographics import collect_demographics
    inputs = iter(['Bob', '25', 'Male'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    demo = collect_demographics()
    assert set(demo.keys()) == {'name', 'age', 'gender'}
    assert demo['name'] == 'Bob'
    assert demo['age'] == '25'
    assert demo['gender'] == 'Male' 