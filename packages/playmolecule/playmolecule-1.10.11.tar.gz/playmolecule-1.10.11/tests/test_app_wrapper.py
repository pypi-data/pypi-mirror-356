from pathlib import Path
import os


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
    print("Running test function with args:", locals())


def test_app_wrapper():
    from playmolecule.devutils import app_wrapper
    import tempfile
    import json

    args_cli = [
        "--outdir",
        "/tmp/outdir",
        "--pdb",
        "/tmp/test.pdb",
        "--simtime",
        "0.3",
        "--equiltimes",
        "0.1 0.2",
        "--randomize",
        "True false",
        "--no-prep",
        "--forcefield",
        "AMBER",
    ]
    args_json = {
        "outdir": "/tmp/outdir",
        "pdb": "/tmp/test.pdb",
        "simtime": 0.3,
        "equiltimes": [0.1, 0.2],
        "randomize": [True, False],
        "no_prep": True,
        "forcefield": "AMBER",
    }

    app_wrapper("playmolecule._test_funcs._test_func", " ".join(args_cli))

    with tempfile.TemporaryDirectory() as tmpdir:
        jsonf = os.path.join(tmpdir, "args.json")
        with open(jsonf, "w") as f:
            json.dump(args_json, f)
        app_wrapper("playmolecule._test_funcs._test_func", input_json=jsonf)


# def test_app_wrapper_pmws(self):
#     import os

#     args = [
#         "--outdir",
#         "/tmp/",
#         "--pdb",
#         "/tmp/test.pdb",
#         "--simtime",
#         "0.3",
#         "--equiltimes",
#         "0.1 0.2",
#         "--randomize",
#         "false True",
#         "--no-prep",
#         "--forcefield",
#         "AMBER",
#     ]
#     app_wrapper2(
#         "playmolecule.devutils._test_func",
#         token=os.environ["PM_TOKEN"],
#         execid="xx",
#     )


def test_app_argparse_dump():
    from playmolecule.devutils import app_wrapper
    import tempfile
    import json

    dump_ref = {
        "name": "TestFunc",
        "version": "1",
        "description": "Test function",
        "params": [
            {
                "mandatory": True,
                "description": "Output directory",
                "type": "Path",
                "name": "outdir",
                "tag": "--outdir",
                "value": None,
                "nargs": None,
                "choices": None,
            },
            {
                "mandatory": True,
                "description": "Input file",
                "type": "Path",
                "name": "pdb",
                "tag": "--pdb",
                "value": None,
                "nargs": None,
                "choices": None,
            },
            {
                "mandatory": False,
                "description": "Simulation time",
                "type": "float",
                "name": "simtime",
                "tag": "--simtime",
                "value": 0.5,
                "nargs": None,
                "choices": None,
            },
            {
                "mandatory": False,
                "description": "List of equilibration times",
                "type": "float",
                "name": "equiltimes",
                "tag": "--equiltimes",
                "value": None,
                "nargs": "+",
                "choices": None,
            },
            {
                "mandatory": False,
                "description": "List of booleans",
                "type": "bool",
                "name": "randomize",
                "tag": "--randomize",
                "value": [True],
                "nargs": "+",
                "choices": None,
            },
            {
                "mandatory": False,
                "description": "No preparation",
                "type": "bool",
                "name": "no_prep",
                "tag": "--no-prep",
                "value": False,
                "nargs": None,
                "choices": None,
            },
            {
                "mandatory": False,
                "description": "The simulation forcefield",
                "type": "str",
                "name": "forcefield",
                "tag": "--forcefield",
                "value": "CHARMM",
                "nargs": None,
                "choices": ["CHARMM", "AMBER"],
            },
        ],
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        argpf = os.path.join(tmpdir, "argp.json")
        app_wrapper("playmolecule._test_funcs._test_func", dump_manifest=argpf)

        with open(argpf, "r") as f:
            argp = json.load(f)
            assert argp == dump_ref
