from climlab.model.column import column_state
from climlab.radiation import GreyGas
from climlab.convection import ConvectiveAdjustment
from climlab.process.couple import couple

def create_grey_gas_model(
    num_lev=30,
    water_depth=2.5,
    adj_lapse_rate=6.5,
    tau=0.83,
    S0=1365.2,
    **kwargs
):
    """
    Creates a single-column Grey Gas Radiative-Convective model.

    This function sets up a single-column atmospheric model that combines a
    "grey" gas radiation scheme with a convective adjustment process. It is a
    classic, simplified model for understanding the basic principles of the
    planetary greenhouse effect and the vertical temperature structure of the
    atmosphere.

    The radiative scheme assumes the atmosphere has a uniform longwave optical
    depth, specified by the `tau` parameter.

    Parameters
    ----------
    num_lev : int, optional
        Number of vertical levels in the atmosphere. Defaults to 30.
    water_depth : float, optional
        The depth of the surface water layer, providing the model's heat capacity.
        Defaults to 2.5 meters.
    adj_lapse_rate : float, optional
        The critical lapse rate for convective adjustment (K/km). Defaults to 6.5 K/km.
    tau : float, optional
        The longwave optical depth of the atmosphere. This parameter controls the
        strength of the greenhouse effect. Defaults to 0.83.
    S0 : float, optional
        The solar constant in W/m^2. Defaults to 1365.2.
    **kwargs : dict
        Additional keyword arguments passed to `climlab.column_state`.

    Returns
    -------
    climlab.process.time_dependent_process.TimeDependentProcess
        A coupled climlab model process ready for integration, combining grey
        gas radiation and convective adjustment.
    """
    state = column_state(num_lev=num_lev, water_depth=water_depth, **kwargs)

    # Longwave and shortwave radiation model (Grey Gas)
    rad = GreyGas(name='Grey Gas Radiation', state=state, tau=tau, S0=S0)

    # Convective adjustment model
    conv = ConvectiveAdjustment(
        name='Convective Adjustment',
        state=state,
        adj_lapse_rate=adj_lapse_rate
    )

    grey_gas_model = couple([rad, conv], name='Grey Gas Model')

    return grey_gas_model
