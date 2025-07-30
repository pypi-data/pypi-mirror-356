from climlab.model.column import column_state
from climlab.radiation import CAM3, ManabeWaterVapor
from climlab.convection import ConvectiveAdjustment
from climlab.process.couple import couple

def create_rce_model(
    num_lev=30,
    water_depth=2.5,
    adj_lapse_rate=6.5,
    S0=1365.2,
    **kwargs
):
    """
    Creates a single-column Radiative-Convective Equilibrium (RCE) model.

    This function sets up a single-column model with coupled processes for
    radiation (CAM3) and convection, with interactive water vapor.

    Parameters
    ----------
    num_lev : int, optional
        Number of vertical levels. Defaults to 30.
    water_depth : float, optional
        Depth of the surface water layer in meters. Defaults to 2.5.
    adj_lapse_rate : float, optional
        The critical lapse rate for convective adjustment in K/km. Defaults to 6.5.
    S0 : float, optional
        The solar constant in W/m^2. Defaults to 1365.2.
    **kwargs : dict
        Additional keyword arguments passed to `climlab.column_state`.

    Returns
    -------
    climlab.process.time_dependent_process.TimeDependentProcess
        A coupled climlab model process ready for integration.
    """
    state = column_state(num_lev=num_lev, water_depth=water_depth, **kwargs)
    
    rad = CAM3(name='Radiation', state=state, S0=S0)
    
    conv = ConvectiveAdjustment(
        name='Convective Adjustment',
        state=state,
        adj_lapse_rate=adj_lapse_rate
    )
    
    h2o = ManabeWaterVapor(name='WaterVapor', state=state)
    rad.specific_humidity = h2o.q

    rce_model = couple([rad, conv, h2o], name='RCE Model')
    return rce_model
