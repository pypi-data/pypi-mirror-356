import tempfile
import subprocess
import shutil
import os
from pathlib import Path
import pytest
from invoke import Context
from invoke.config import Config
import yaml

@pytest.mark.integration
def test_airoh_template_smoke():
    """
    Clone the airoh-template repo (from invoke config), run setup, fetch, and run.
    Docker is skipped by default.
    """
    invoke_config_path = Path(__file__).parents[1] / "invoke.yaml"
    with open(invoke_config_path, "r") as f:
        overrides = yaml.safe_load(f)
    config = Config(overrides=overrides)
    c = Context(config=config)
    template_url = c.config.get("template_repo")
    assert template_url, "No 'template_repo' defined in invoke.yaml."

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        subprocess.run(["git", "clone", template_url, str(tmpdir_path)], check=True)

        env = {"PYTHONUNBUFFERED": "1", **os.environ}

        # 👇 Install local airoh from this repo before calling invoke in the template
        subprocess.run(["pip", "install", "-e", str(Path(__file__).parents[1])], check=True, env=env)

        subprocess.run(["invoke", "setup"], cwd=tmpdir_path, check=True, env=env)
        subprocess.run(["invoke", "fetch"], cwd=tmpdir_path, check=True, env=env)
        subprocess.run(["invoke", "run"], cwd=tmpdir_path, check=True, env=env)

        output_dir = tmpdir_path / "output_data"
        assert output_dir.exists(), "Output directory was not created."
        assert any(output_dir.iterdir()), "Output directory is empty."

        print("✅ Airoh template smoke test succeeded.")

