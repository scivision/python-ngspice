#!/usr/bin/env python3

import argparse
import subprocess
from matplotlib.pyplot import figure, show
from pathlib import Path
import tempfile

from ngspice_binary import parse_ngspice_raw_binary, get_exe

p = argparse.ArgumentParser(description="Run and plot an ngspice netlist")
p.add_argument("net", help="path to netlist")
args = p.parse_args()

net = Path(args.net)
assert net.is_file(), f"{net} not found"

with tempfile.NamedTemporaryFile() as dat_file:
    # Use ngspice -r to write a Spice3f5 binary file to dat_file.
    subprocess.check_call([
        get_exe("ngspice"), "-b", "-r", dat_file.name, str(net)
    ])
    dat = parse_ngspice_raw_binary(dat_file.name)

cols_lower = {c.lower(): c for c in dat.columns}

if "time" not in cols_lower:
    raise ValueError("No time vector found in ngspice raw file")

time = dat[cols_lower["time"]]
voltage_cols = [c for c in dat.columns if c.lower().startswith("v(")]
# i(v_rss) is reserved for input impedance; exclude it from the current subplot
current_cols = [c for c in dat.columns if c.lower().startswith("i(") and c.lower() != "i(v_rss)"]

if not voltage_cols:
    raise ValueError("No voltage vectors found in ngspice raw file")
if not current_cols:
    raise ValueError("No current vectors found in ngspice raw file")

has_impedance = "v(vin)" in cols_lower and "i(v_rss)" in cols_lower
nplots = 3 if has_impedance else 2

fig = figure(1)
axes = fig.subplots(nplots, 1, sharex=True)
ax_v, ax_i = axes[0], axes[1]

for col in voltage_cols:
    ax_v.plot(time, dat[col], label=col)
ax_v.grid(True)
ax_v.set_ylabel("Node Voltage [V]")
ax_v.legend(loc="best")
ax_v.set_title(f"Voltage Multiplier: {net.stem}")

for col in current_cols:
    ax_i.plot(time, dat[col], label=col)
ax_i.grid(True)
ax_i.set_ylabel("Device Current [A]")
ax_i.legend(loc="best")

if has_impedance:
    ax_z = axes[2]
    zmag = (dat[cols_lower["v(vin)"]] / dat[cols_lower["i(v_rss)"]]).abs()
    ax_z.plot(time, zmag)
    ax_z.grid(True)
    ax_z.set_ylabel("|Zin| [Ω]")

axes[-1].set_xlabel("Time [s]")

show()
