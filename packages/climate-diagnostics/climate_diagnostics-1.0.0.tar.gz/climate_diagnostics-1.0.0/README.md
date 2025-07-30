# Climate Diagnostics Toolkit

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)
[![PyPI version](https://img.shields.io/pypi/v/climate_diagnostics.svg)](https://pypi.org/project/climate_diagnostics/)

A Python package for analyzing and visualizing climate data and running simple climate models, integrated directly with xarray.

## Overview

The Climate Diagnostics Toolkit provides powerful tools to process, analyze, and visualize climate data using xarray accessors, and to create, run, and analyze a hierarchy of well-established simple climate models using `climlab`. The package offers functionality for seasonal filtering, spatial averaging, trend analysis, time series decomposition, and creating instances of models ranging from simple Energy Balance Models (EBMs) to Radiative-Convective Models (RCMs) with multi-band radiation schemes.

## Features

* **Data Analysis with xarray Accessors**:
  * Access analysis functions via `.climate_timeseries`, `.climate_trends`, and `.climate_plots` on your `xarray.Dataset` objects.
  * Filter data by meteorological seasons, and select spatial and temporal domains.
  * Decompose time series using STL and compute robust spatial trends with Dask for parallelization.
  * Generate publication-quality spatial maps with Cartopy.

* **Climate Model Hierarchy (via `.models` submodule)**:
  * Create, configure, and run a suite of classic climate models from the `climlab` library.
  * The submodule provides simple creator functions for complex models, making it easy to get started with climate modeling.
  * Implemented models include:
    * **Energy Balance Model (EBM)**: `create_ebm_model()` - A latitudinally-dependent model for studying ice-albedo feedback and heat transport.
    * **Boltzmann EBM**: `create_boltzmann_ebm_model()` - An EBM using the fundamental Stefan-Boltzmann law for outgoing radiation.
    * **Radiative-Convective Equilibrium (RCE)**: `create_rce_model()` - A single-column model using the sophisticated CAM3 radiation scheme to study atmospheric equilibrium.
    * **Grey Gas RCM**: `create_grey_gas_model()` - A classic RCM that represents the greenhouse effect with a single atmospheric optical depth.
    * **Band RCM**: `create_band_rcm_model()` - An advanced column model with a multi-band radiation scheme for CO2, O3, and H2O.

## Installation

```bash
pip install climate-diagnostics
```

## Usage Examples

### Analyzing Trends
```python
import xarray as xr
# The accessors are registered automatically on import
import climate_diagnostics

# Load data
ds = xr.open_dataset("path/to/climate_data.nc")

# Calculate and plot spatial trends per decade
spatial_trends = ds.climate_trends.calculate_spatial_trends(
    variable="air",
    level=850,
    season="annual",
    num_years=10,  # Trend per decade
)
```

### Creating and Running a Climate Model
```python
from climate_diagnostics import models

# Create an Energy Balance Model with a slightly lower ice albedo
ebm = models.create_ebm_model(ai=0.55)

# Integrate the model for 5 years
ebm.integrate_years(5)

# You can now access the model's state, e.g., the surface temperature
print(ebm.Ts)

# All models are climlab objects, so you can use climlab's tools for analysis
# For example, let's create a Radiative-Convective model and check its equilibrium
rce = models.create_rce_model(water_depth=10)
rce.integrate_years(2)
print(rce.ASR - rce.OLR) # Check the energy balance
```

## Dependencies

- xarray
- dask
- netCDF4
- bottleneck
- matplotlib
- numpy
- scipy
- cartopy
- statsmodels
- **climlab**

## Development

```bash
git clone https://github.com/pranay-chakraborty/climate_diagnostics.git
cd climate_diagnostics
# Set up environment (conda recommended)
pip install -e ".[dev]"
```

## License

[MIT LICENSE](LICENSE)

## Citation

If you use Climate Diagnostics Toolkit in your research, please cite:

```
Chakraborty, P. (2025) & Muhammed I. K., A. (2025). Climate Diagnostics Toolkit: Tools for analyzing and visualizing climate data using xarray accessors. Version 1.0.0. https://github.com/pranay-chakraborty/climate_diagnostics
```

For LaTeX users:

```bibtex
@software{chakraborty2025climate,
  author = {Chakraborty, Pranay and Muhammed I. K., Adil},
  title = {{Climate Diagnostics Toolkit: Tools for analyzing and visualizing climate data using xarray accessors}},
  year = {2025},
  version = {1.0.0},
  publisher = {GitHub},
  url = {https://github.com/pranay-chakraborty/climate_diagnostics},
  note = {[Computer software]}
}
```