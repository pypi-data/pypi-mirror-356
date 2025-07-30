"""
The `models` submodule provides functions to create and configure
standard climate model configurations using the `climlab` toolkit.
"""
from .rce import create_rce_model
from .grey_gas import create_grey_gas_model
from .ebm import create_ebm_model
from .boltzmann_ebm import create_boltzmann_ebm_model
from .band_rcm import create_band_rcm_model

__all__ = [
    'create_rce_model',
    'create_grey_gas_model',
    'create_ebm_model',
    'create_boltzmann_ebm_model',
    'create_band_rcm_model',
]
