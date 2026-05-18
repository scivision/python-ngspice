import pandas
import numpy
import functools
import shutil

__all__ = ["parse_ngspice_dc_tables", "parse_ngspice_raw_binary"]


@functools.cache
def get_exe(name: str) -> str:
    exe = shutil.which(name)
    if exe is None:
        raise FileNotFoundError(f"{name} not found in PATH")

    return exe


def parse_ngspice_dc_tables(text: str) -> pandas.Series:
    data = {}
    lines = text.replace("\x0c", "\n").splitlines()

    for i, line in enumerate(lines):
        if not line.strip().startswith("Index"):
            continue

        headers = line.split()
        row = None
        for candidate in lines[i + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                continue
            if stripped.startswith("Index"):
                break
            if stripped.startswith("0"):
                row = stripped.split()
                break

        if row is None:
            continue

        for key, val in zip(headers[1:], row[1:]):
            try:
                data[key] = float(val)
            except ValueError:
                pass

    if not data:
        raise ValueError("Could not parse DC data rows from ngspice output")

    return pandas.Series(data)


def parse_ngspice_raw_binary(path: str) -> pandas.DataFrame:
    """Parse a Spice3f5 raw file and return the most useful plot as a DataFrame.

    Supports both `Binary:` and `Values:` data sections.
    """
    plots: list[pandas.DataFrame] = []

    with open(path, "rb") as fh:
        while True:
            lineb = fh.readline()
            if not lineb:
                break

            line = lineb.decode("latin1", errors="replace").strip()
            if not line.startswith("Title:"):
                continue

            flags = "real"
            no_vars = None
            no_points = None
            variables: list[str] = []

            while True:
                metab = fh.readline()
                if not metab:
                    break

                row = metab.decode("latin1", errors="replace").strip()

                if row.startswith("Flags:"):
                    flags = row.split(":", 1)[1].strip().lower()
                elif row.startswith("No. Variables:"):
                    no_vars = int(row.split(":", 1)[1].strip())
                elif row.startswith("No. Points:"):
                    no_points = int(row.split(":", 1)[1].strip())
                elif row == "Variables:":
                    if no_vars is None:
                        raise ValueError("Malformed ngspice raw header: missing No. Variables")
                    for _ in range(no_vars):
                        vline = fh.readline().decode("latin1", errors="replace").strip()
                        parts = vline.split()
                        if len(parts) < 2:
                            raise ValueError(f"Malformed ngspice variable row: {vline!r}")
                        variables.append(parts[1])
                elif row == "Binary:":
                    if no_vars is None or no_points is None:
                        raise ValueError("Malformed ngspice raw header: missing data dimensions")

                    if "complex" in flags:
                        raw = numpy.fromfile(fh, dtype=numpy.float64, count=no_points * no_vars * 2)
                        if raw.size != no_points * no_vars * 2:
                            raise ValueError("Unexpected EOF while reading complex ngspice raw data")
                        arr = raw.reshape(no_points, no_vars, 2)[:, :, 0]
                    else:
                        raw = numpy.fromfile(fh, dtype=numpy.float64, count=no_points * no_vars)
                        if raw.size != no_points * no_vars:
                            raise ValueError("Unexpected EOF while reading ngspice raw data")
                        arr = raw.reshape(no_points, no_vars)

                    plots.append(pandas.DataFrame(arr, columns=variables))
                    break
                elif row == "Values:":
                    if no_vars is None or no_points is None:
                        raise ValueError("Malformed ngspice raw header: missing data dimensions")

                    vals: list[float] = []
                    needed = no_points * no_vars
                    while len(vals) < needed:
                        vlineb = fh.readline()
                        if not vlineb:
                            break

                        vrow = vlineb.decode("latin1", errors="replace").strip()
                        if not vrow:
                            continue

                        parts = vrow.split()
                        if parts and parts[0].isdigit():
                            parts = parts[1:]

                        for token in parts:
                            try:
                                vals.append(float(token))
                            except ValueError:
                                # Ignore non-numeric tokens in ascii value sections.
                                pass

                    if len(vals) < needed:
                        raise ValueError("Unexpected EOF while reading ngspice ascii raw data")

                    arr = numpy.array(vals[:needed], dtype=numpy.float64).reshape(no_points, no_vars)
                    plots.append(pandas.DataFrame(arr, columns=variables))
                    break

    if not plots:
        raise ValueError("No data plots found in ngspice raw file")

    with_time = [df for df in plots if any(c.lower() == "time" for c in df.columns)]
    if with_time:
        return max(with_time, key=len)

    return max(plots, key=len)
