#!/usr/bin/env python3

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy
from matplotlib.pyplot import figure, show

from ngspice_binary import get_exe, parse_ngspice_raw_binary

p = argparse.ArgumentParser(description="Run ngspice AC analysis and plot input impedance spectrum")
p.add_argument("net", help="path to AC netlist")
args = p.parse_args()

net = Path(args.net)
assert net.is_file(), f"{net} not found"

with tempfile.NamedTemporaryFile() as dat_file:
    subprocess.check_call([get_exe("ngspice"), "-b", "-r", dat_file.name, str(net)])
    dat = parse_ngspice_raw_binary(dat_file.name)

cols_lower = {c.lower(): c for c in dat.columns}
if "frequency" not in cols_lower:
    raise ValueError("No frequency vector found in ngspice raw file")
if "v(vin)" not in cols_lower:
    raise ValueError("Missing v(vin) vector in ngspice raw file")
if "i(v_rss)" not in cols_lower:
    raise ValueError("Missing i(v_rss) vector in ngspice raw file")

freq = numpy.asarray(dat[cols_lower["frequency"]], dtype=float)
vin = dat[cols_lower["v(vin)"]]
iin = dat[cols_lower["i(v_rss)"]]

zin = vin / iin
zmag = numpy.abs(zin)

fig = figure(3)
ax = fig.subplots(1, 1)
ax.semilogx(freq, zmag, label="|Zin| = |V(vin)/I(v_rss)|")
ax.grid(True, which="both")
ax.set_ylabel("Impedance [Ohm]")
ax.set_xlabel("Frequency [Hz]")
ax.set_title(f"AC Input Impedance Spectrum: {net.stem}")
ax.legend(loc="best")

show()
