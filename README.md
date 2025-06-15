# EPEX-AT-History

This repository contains historic data from [EPEX spot market](https://www.epexspot.com) for Austria, from [awattar.at](https://www.awattar.at/services/api).

Data available from 2014-01-01. Useful for statistical analysis of hourly stock market prices.

Inspired by [EPEX-DE-History](https://github.com/elgohr/EPEX-DE-History).

Older data (currently before 2025-01-01) may be archived in the `archive` folder.
Run the following to extract archived data into the `data` folder:

```
python restore_historic.py
```
