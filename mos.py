#!/usr/bin/env python3

import argparse
import subprocess
from matplotlib.pyplot import figure, show
from pathlib import Path
import tempfile

from ngspice_binary import parse_ngspice_raw_binary, get_exe

p = argparse.ArgumentParser(description="Run and plot an ngspice MOSFET netlist")
p.add_argument("net", nargs="?", default="archive/mos.net",
               help="path to netlist (default: archive/mos.net)")
args = p.parse_args()

net = Path(args.net)
assert net.is_file(), f"{net} not found"

with tempfile.NamedTemporaryFile() as dat_file:
    subprocess.check_call([get_exe("ngspice"), "-b", "-r", dat_file.name, str(net)])
    dat = parse_ngspice_raw_binary(dat_file.name)

cols_lower = {c.lower(): c for c in dat.columns}
if "time" not in cols_lower:
    raise ValueError("No time vector found in ngspice raw file")

time = dat[cols_lower["time"]]
voltage_cols = [c for c in dat.columns if c.lower().startswith("v(")]

if not voltage_cols:
    raise ValueError("No voltage vectors found in ngspice raw file")

fig = figure(2)
ax = fig.subplots(1, 1)
for col in voltage_cols:
    ax.plot(time, dat[col], label=col)
ax.grid(True)
ax.set_ylabel("Node Voltage [V]")
ax.set_xlabel("Time [s]")
ax.legend(loc="best")
ax.set_title(f"MOSFET: {net.stem}")

show()
