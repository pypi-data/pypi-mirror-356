from pathlib import Path
from func2argparse import func_to_manifest, manifest_to_argparser


def _test_func(
    outdir: Path,
    pdb: Path,
    simtime: float = 0.5,
    equiltimes: list[float] = None,
    randomize: list[bool] = [True],
    no_prep: bool = False,
    forcefield: str = "CHARMM",
    **kwargs,
):
    """TestFunc

    Test function

    Parameters
    ----------
    outdir : Path
        Output directory
    pdb : Path
        Input file
    simtime : float
        Simulation time
    equiltimes : list[float]
        List of equilibration times
    randomize : list[bool]
        List of booleans
    no_prep : bool
        No preparation
    forcefield : str, choices=("CHARMM", "AMBER")
        The simulation forcefield
    """
    assert outdir == "/tmp/outdir"
    assert pdb == "/tmp/test.pdb"
    assert simtime == 0.3
    assert equiltimes == [0.1, 0.2]
    assert randomize == [True, False]
    assert no_prep
    assert forcefield == "AMBER"

    print("Running test function with args:", locals())


def get_argparser():
    return manifest_to_argparser(__manifest__)


__manifest__ = func_to_manifest(_test_func, __file__)


if __name__ == "__main__":
    # Basic test to ensure all parameters work
    parser = get_argparser()
    parser.print_help()
