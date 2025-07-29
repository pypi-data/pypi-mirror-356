import pytest
import shutil
import tempfile
import numpy as np
import pandas as pd
from pathlib import Path
from types import SimpleNamespace
import json
import joblib

from neuralk_foundry_ce.workflow import WorkFlow, Step, Field


# Define a minimal DummyStep for testing
class DummyStep(Step):
    inputs = [Field('x', '')]
    outputs = [Field('y', '')]

    def __init__(self, name, increment):
        self.name = name
        self.increment = increment
        self.logged_metrics = {}
        self.namespace = None

    def run(self, inputs):
        x = inputs["x"]
        y = x + self.increment
        self.logged_metrics = {"increment": self.increment}
        return {"x": x + self.increment, "y": y}


# TESTS

def test_workflow_runs_and_produces_expected_output():
    wf = WorkFlow(
        steps=[
            DummyStep(name="add2", increment=2),
            DummyStep(name="add3", increment=3)
        ],
        cache_dir=Path(tempfile.mkdtemp())
    )
    result, metrics = wf.run({"x": 5})
    assert result["y"] == 10
    assert metrics["add3"]["increment"] == 3
    shutil.rmtree(wf.cache_dir)

def test_workflow_caching_mechanism():
    cache_dir = Path(tempfile.mkdtemp())
    wf = WorkFlow(steps=[DummyStep(name="add5", increment=5)], cache_dir=cache_dir)
    _ = wf.run({"x": 10})
    # Ensure cache directory exists
    assert (cache_dir / "0_add5").exists()
    assert (cache_dir / "0_add5" / "_scalars.json").exists()
    shutil.rmtree(cache_dir)

def test_check_consistency_raises_on_missing_input():
    wf = WorkFlow(steps=[DummyStep(name="needs_x", increment=1)], cache_dir=Path(tempfile.mkdtemp()))
    with pytest.warns(UserWarning, match="requires unavailable fields"):
        result = wf.check_consistency(init_keys={})
    assert (not result)
    shutil.rmtree(wf.cache_dir)

def test_workflow_metrics_are_collected_per_step():
    wf = WorkFlow(
        steps=[
            DummyStep(name="step1", increment=1),
            DummyStep(name="step2", increment=2),
        ],
        cache_dir=Path(tempfile.mkdtemp())
    )
    _, metrics = wf.run({"x": 0})
    assert metrics["step1"]["increment"] == 1
    assert metrics["step2"]["increment"] == 2
    shutil.rmtree(wf.cache_dir)

def test_cache_files_are_created_correctly():
    cache_dir = Path(tempfile.mkdtemp())
    wf = WorkFlow(
        steps=[DummyStep(name="adder", increment=4)],
        cache_dir=cache_dir
    )
    _ = wf.run({"x": np.arange(10)})
    step_dir = cache_dir / "0_adder"
    assert step_dir.exists()
    assert any(f.name.startswith("y") for f in step_dir.iterdir() if f.name.endswith(".npy") or f.name.endswith(".json"))
    shutil.rmtree(cache_dir)
