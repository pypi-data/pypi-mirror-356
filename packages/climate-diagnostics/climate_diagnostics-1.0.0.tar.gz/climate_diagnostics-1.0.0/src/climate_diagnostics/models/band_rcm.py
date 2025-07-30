from climlab.model.column import BandRCModel

def create_band_rcm_model(
    num_lev=30,
    water_depth=2.5,
    adj_lapse_rate=6.5,
    co2_vmr=3.8e-4,
    S0=1365.2,
    **kwargs
):
    """
    Creates a single-column Radiative-Convective Model with a multi-band
    spectral radiation scheme.

    This function initializes the `climlab.BandRCModel`, which provides a more
    spectrally detailed representation of radiation than a grey gas model.
    The model divides the spectrum into three shortwave and four longwave bands,
    allowing for distinct absorption properties for different gases like CO2,
    O3, and H2O.

    The model is configured with interactive water vapor (fixed relative humidity)
    and convective adjustment. By default, it has no ozone, but this can be
    configured via keyword arguments.

    Parameters
    ----------
    num_lev : int, optional
        Number of vertical levels. Defaults to 30.
    water_depth : float, optional
        Depth of the surface water layer in meters. Defaults to 2.5.
    adj_lapse_rate : float, optional
        The critical lapse rate for convective adjustment in K/km. Defaults to 6.5.
    co2_vmr : float, optional
        The volume mixing ratio of CO2. Defaults to 3.8e-4 (380 ppm).
    S0 : float, optional
        The solar constant in W/m^2. Defaults to 1365.2.
    **kwargs : dict
        Additional keyword arguments passed to the `climlab.BandRCModel`.

    Returns
    -------
    climlab.model.column.BandRCModel
        An initialized `climlab` Band RCM process, ready for integration.
    """
    # Initialize the BandRCModel with relevant parameters
    band_model = BandRCModel(
        num_lev=num_lev,
        water_depth=water_depth,
        adj_lapse_rate=adj_lapse_rate,
        **kwargs
    )
    
    # Set the volume mixing ratios for radiatively active gases
    band_model.absorber_vmr['CO2'] = co2_vmr
    
    # Set the solar constant on the insolation subprocess
    band_model.subprocess['insolation'].S0 = S0
    
    return band_model
