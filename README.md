# Python - command line SPICE interface and plotting

GNUcap or
[NGspice](https://ngspice.sourceforge.io/)
voltage multiplier sim.

Used for my Ph.D. qualifying exam, and a follow-on to my
[harmonic radar tag improvements](https://www.scivision.dev/harmonic-radar).

NOTE: Consider using
[PySpice](https://pyspice.fabrice-salvaire.fr)
instead of this approach.

Installation:

* Linux: `apt install ngspice`
* macOS: `brew install ngspice`
* [Windows](https://ngspice.sourceforge.io/download.html)

```sh
python -m pip install -e ./
```

## Simulations

Simluate single-stage voltage doubler plotting voltage and current vs. time.

```sh
python voltageDoubler.py archive/vDub.net
```

Simulate multi-stage voltage multiplier plotting voltage, current, and impedance vs. time.

```sh
python voltageDoubler.py archive/vDubMult.net
```

Simulate no-driver Cree XHP LED problems due to wire voltage drop, using `ledDrop.net` and io.StringIO with stdout.

```sh
python ledDrop.py
```

* `runDubTry.m` plot spectrum
* `runMos.m` using MOS simulation
