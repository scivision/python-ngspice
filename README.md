# Python - command line ngSPICE interface and plotting

[NGspice](https://ngspice.sourceforge.io/)
simluations using Python matplotlib for plotting.

Used for my Ph.D. qualifying exam, and a follow-on to my
[harmonic radar tag improvements](https://www.scivision.dev/harmonic-radar).

This file-based approach is an alternative to CFFI
[PySpice](https://github.com/PySpice-org/PySpice).

Installation:

* Linux: `apt install ngspice`
* macOS: `brew install ngspice`
* [Windows](https://ngspice.sourceforge.io/download.html)

Setup this package:

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

Simulatie impedance vs. frequency for multi-stage voltage multiplier.

```sh
python impedance.py archive/vDubTry.net
```

Simulate no-driver Cree XHP LED problems due to wire voltage drop, using `ledDrop.net` and io.StringIO with stdout.

```sh
python ledDrop.py
```

Simulate MOSFET saturated output.

```sh
python mos.py archive/mos.net
```
