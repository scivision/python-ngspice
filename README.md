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


Simulate no-driver Cree XHP LED problems due to wire voltage drop, using `ledDrop.net` and io.StringIO to avoid output file mess.

```sh
python ledDrop.py
```

### Other programs

These programs run from GNU Octave or Matlab.

* `runDub.m` run and plot basic voltage doubler current input and voltage output vs. time
* `runDubTry.m` plot spectrum
* `runDubMult.m` multi-stage voltage multiplier: voltage, current, impedance
* `runMos.m` using MOS simulation
