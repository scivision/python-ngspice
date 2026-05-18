#!/usr/bin/env python3

import subprocess
from matplotlib.pyplot import figure, show
from pathlib import Path
import tempfile

from utils import get_exe
from ngspice import parse_ngspice_raw_binary


net = Path(__file__).parent.joinpath("archive/vDub.net")
assert net.is_file(), f"{net} not found"

with tempfile.NamedTemporaryFile() as dat_file:
    # Use ngspice -r to write a Spice3f5 binary file to dat_file.
    subprocess.check_call([
        get_exe("ngspice"), "-b", "-r", dat_file.name, str(net)
    ])

    dat = parse_ngspice_raw_binary(dat_file.name)

required_cols = [
    "time",
    "v(vin)",
    "v(1)",
    "v(vdcout)",
    "i(v_c1s)",
    "i(v_c2s)",
    "i(v_d1s)",
    "i(v_d2s)",
]
missing = [name for name in required_cols if not any(c.lower() == name for c in dat.columns)]
if missing:
    raise ValueError(f"Missing required ngspice columns in {dat_file}: {missing}")


def get_col(df, name: str) -> str:
    columns = {c.lower(): c for c in df.columns}
    key = name.lower()
    if key not in columns:
        raise KeyError(f"Expected column {name!r} not found in ngspice output")
    return columns[key]


time = dat[get_col(dat, "time")]

voltage_cols = [get_col(dat, "v(vin)"), get_col(dat, "v(1)"), get_col(dat, "v(vdcout)")]
current_cols = [
    ("i(C1)", get_col(dat, "i(v_c1s)")),
    ("i(C2)", get_col(dat, "i(v_c2s)")),
    ("i(D1)", get_col(dat, "i(v_d1s)")),
    ("i(D2)", get_col(dat, "i(v_d2s)")),
]

fig = figure(1)
ax_v, ax_i = fig.subplots(2, 1, sharex=True)

for col in voltage_cols:
    ax_v.plot(time, dat[col], label=col)

ax_v.grid(True)
ax_v.set_ylabel("Node Voltage [V]")
ax_v.legend(loc="best")
ax_v.set_title("Basic Voltage Doubler Voltages")

for label, col in current_cols:
    ax_i.plot(time, dat[col], label=label)

ax_i.grid(True)
ax_i.set_ylabel("Device Current [A]")
ax_i.set_xlabel("Time [s]")
ax_i.legend(loc="best")
ax_i.set_title("Basic Voltage Doubler Currents")

show()
