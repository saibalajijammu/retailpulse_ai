from pathlib import Path


def test_home_exists():
    assert Path("Home.py").exists()