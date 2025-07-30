# NATURESCAPES `shoreline` Package
![PyPI - Format](https://img.shields.io/pypi/format/shoreline?link=https%3A%2F%2Fpypi.org%2Fproject%2Fshoreline%2F)

This is the repo for the Naturescapes `shoreline` package and research notebooks.

Utilities for ray casting, working with LineString resolution, and clipping rays have been organized as a Python package in the `src` directory. The main interface is provided by the `ShorelineAnalyzer` class.

**The minimum supported Python version is Python 3.10**.

## Usage (see `shoreline.ipynb` for example)
```python
from shoreline import ShorelineAnalyzer

# Create a new analyzer
analyzer = ShorelineAnalyzer()
sa = ShorelineAnalyzer(
    crs="EPSG:25829",
    shoreline="geodata/ireland/gadm36_IRL_shp/gadm36_IRL_0.shp",
    tideline="geodata/cleanup/Calculated Contours Backup/vorf_lat_simplified.gpkg",
    hat=2.09,
    lat=-2.44,
    wave_period=3.0,
    wave_height=2.0,
    ray_resolution=10,
    smoothing_window=500, # optional, defaults to 250
    origin_angle=0, # angle at which waves travel towards LAT; 0 is north, positive is clockwise
    origin_distance=1500 # distance in m from LAT bbox at which wave rays originate 
)
analysis = sa.evaluate()
# we now have a result object containing analysis metadata (.metadata), as well as geometries
# and summary stats
# call help(analysis) for more

# we can plot results if we're using a notebook. pl is a tuple of Matplotlib figures
pl = analysis.visualise_coastal_slopes()
# this gives us a (map, stats) tuple. Each figure can be saved
pl[0].savefig("dublin.png", dpi=300, bbox_inches="tight")
# you can also call the analysis.summary_stats property
# the computed ray and slope DataFrame is available as analysis.ray_data
```

## Sample output from [`shoreline.ipynb`](isobath_to_onshore.ipynb) (Dublin Bay)
![Dublin Bay](standard.png "Dublin Bay, with smoothed rays cast offshore to onshore")

## Sample output of a ray intersecting isobaths [`ray_slope.ipynb`](ray_slope.ipynb)
![Ray / Slope](ray_slope.png "Using a divergent colour scheme to visualise slope orientation")

# Installation
`uv add shoreline` or `pip install shoreline`

## Installing for local development
This project is developed using [`uv`](https://docs.astral.sh/uv/),  but should work with just pip. The use of a virtualenv is advised.

```shell
uv venv
source .venv/bin/activate
uv sync --all-extras

uv add --dev ipykernel
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=shoreline
uv run --with jupyter jupyter lab
```
When creating a notebook, select the **`shoreline`** kernel from the dropdown. Then use e.g. `!uv add pydantic` to add pydantic to the project's dependencies, or `!uv pip install pydantic` to install pydantic into the project's virtual environment without persisting the change to the project `pyproject.toml` or `uv.lock files`. Either command will make import pydantic work within the notebook

### Anaconda
For Anaconda users: you will probably have to pull the requirements out of `pyproject.toml`. Sorry!

## Testing
The smoothing algorithm is relatively well covered by tests (see `tests/test_utils.py`). Run `pytest` in the root dir in order to test if you'd like to tinker with it.

## Data
Are in the [`geodata`](geodata) folder.

## Copyright
Stephan Hügel / Naturescapes, 2025

## Funding
The NATURESCAPES project is funded by the European Union under Grant Agreement No 10108434
