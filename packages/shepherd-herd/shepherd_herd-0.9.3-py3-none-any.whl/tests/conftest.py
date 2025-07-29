import time
from pathlib import Path
from shutil import copy

import numpy as np
import pytest
import yaml
from click.testing import CliRunner
from shepherd_data import Writer
from shepherd_herd import Herd
from shepherd_herd.herd import path_xdg_config
from shepherd_herd.herd_cli import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def extract_first_sheep(herd_path: Path) -> str:
    with herd_path.open(encoding="utf-8-sig") as stream:
        try:
            inventory_data = yaml.safe_load(stream)
        except yaml.YAMLError as _xpt:
            msg = f"Couldn't read inventory file {herd_path.as_posix()}"
            raise TypeError(msg) from _xpt
    return next(iter(inventory_data["sheep"]["hosts"].keys()))


def wait_for_end(cli_runner: CliRunner, tmin: float = 0, timeout: float = 999) -> bool:
    ts_start = time.time()
    while cli_runner.invoke(cli, ["status"]).exit_code > 0:
        duration = time.time() - ts_start
        if duration > timeout:
            msg = f"Shepherd ran into timeout ({timeout} s)"
            raise TimeoutError(msg)
        time.sleep(2)
    duration = time.time() - ts_start
    if duration < tmin:
        msg = f"Shepherd only took {duration} s (min = {tmin} s)"
        raise TimeoutError(msg)
    return False


def generate_h5_file(file_path: Path, file_name: str = "harvest_example.h5") -> Path:
    store_path = file_path / file_name

    with Writer(store_path, compression=None) as file:
        file.store_hostname("artificial")
        duration_s = 2
        repetitions = 10
        timestamp_vector = np.arange(0.0, duration_s, file.sample_interval_ns / 1e9)

        # values in SI units
        voltages = np.linspace(3.30, 1.90, int(file.samplerate_sps * duration_s))
        currents = np.linspace(100e-6, 2000e-6, int(file.samplerate_sps * duration_s))

        for idx in range(repetitions):
            timestamps = idx * duration_s + timestamp_vector
            file.append_iv_data_si(timestamps, voltages, currents)

    return store_path


@pytest.fixture
def data_h5_path(tmp_path: Path) -> Path:
    return generate_h5_file(tmp_path)


@pytest.fixture
def local_herd(tmp_path: Path) -> Path:
    # locations copied from herd.__innit__()
    inventories: list[Path] = [
        Path().cwd() / "herd.yaml",
        Path().cwd() / "inventory/herd.yaml",
        Path("~").expanduser() / "herd.yaml",
        path_xdg_config / "shepherd/herd.yaml",
        Path("/etc/shepherd/herd.yaml"),
    ]
    host_path = None
    for inventory in inventories:
        if Path(inventory).exists():
            host_path = Path(inventory)
    if host_path is None:
        raise FileNotFoundError(", ".join(inventories))
    local_path = tmp_path / "herd.yaml"
    copy(host_path, local_path)

    return local_path


@pytest.fixture
def _herd_alive() -> None:
    # pre-test is good for start of new test-file
    for _ in range(3):
        time.sleep(1)
        with Herd() as herd:
            if len(herd.group) > 0:
                time.sleep(1)
                return
    raise RuntimeError("No Sheep seems to be alive")


@pytest.fixture
def _herd_stopped(cli_runner: CliRunner, _herd_alive: None) -> None:
    cli_runner.invoke(cli, ["-v", "stop"])
    wait_for_end(cli_runner)
    # make sure kernel module is active
    cli_runner.invoke(
        cli,
        [
            "-v",
            "fix",
        ],
    )
