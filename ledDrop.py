#!/usr/bin/env python3

import subprocess
from matplotlib.pyplot import figure, show
from scipy.interpolate import interp1d

from ngspice import parse_ngspice_dc_tables
from utils import get_exe

# %% brightness from XHP50 datasheet
# https://www.cree-led.com/products/leds/xlamp/xhp/
B1 = [0.2, 0.4, 0.6, 0.8, 1, 1.2]
I1 = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85]
f = interp1d(I1, B1, "cubic")
# %% run sim
ret = subprocess.check_output([get_exe("ngspice"), "-b", "ledDrop.net"], text=True)

dat = parse_ngspice_dc_tables(ret)

ind = ["@d1[id]", "@d6[id]", "@d12[id]"]
names = ["D1", "D6", "D12"]
Iled = dat[ind]
bi = f(Iled)

ax = figure(1).gca()
ax.stem(dat.index, dat.values)  # type: ignore[arg-type]

ax = figure(2).gca()
ax.set_title("LED brightness")
ax.set_ylabel("brightness (normalized)")
ax.stem(names, bi)

show()
