import pandas


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
