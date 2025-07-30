from climlab.model.ebm import EBM

def create_ebm_model(
    num_lat=90,
    water_depth=10.0,
    S0=1365.2,
    A=210.0,
    B=2.0,
    D=0.555,
    Tf=-10.0,
    ai=0.62,
    **kwargs
):
    """
    Creates a latitudinally-dependent Energy Balance Model (EBM).

    This function initializes a pre-configured EBM based on the `climlab.EBM`
    class. It simulates surface temperature (`Ts`) on a latitude grid,
    incorporating key climate processes.

    Parameters
    ----------
    num_lat : int, optional
        Number of latitude bands. Defaults to 90.
    water_depth : float, optional
        Depth of the ocean mixed layer in meters, which sets the heat capacity.
        Defaults to 10.0.
    S0 : float, optional
        The solar constant in W/m^2. Defaults to 1365.2.
    A : float, optional
        The constant part of the linearized outgoing longwave radiation (OLR)
        scheme (OLR = A + B*T). In W/m^2. Defaults to 210.0.
    B : float, optional
        The temperature-dependent part of the linearized OLR scheme. In W/m^2/K.
        Defaults to 2.0.
    D : float, optional
        The meridional heat diffusion coefficient. In W/m^2/K. Defaults to 0.555.
    Tf : float, optional
        The freezing temperature in degrees Celsius below which the surface is
        considered ice-covered for albedo calculations. Defaults to -10.0.
    ai : float, optional
        The albedo of an ice-covered surface. Defaults to 0.62.
    **kwargs : dict
        Additional keyword arguments passed to the `climlab.EBM` constructor.

    Returns
    -------
    climlab.model.ebm.EBM
        An initialized `climlab` EBM process, ready for integration.

    Example
    -------
    >>> from climate_diagnostics.models import create_ebm_model
    >>> # Create an EBM with default parameters
    >>> ebm = create_ebm_model()
    >>> # Integrate the model to equilibrium
    >>> ebm.integrate_years(5)
    >>> # Check the global mean surface temperature
    >>> print(ebm.global_mean_temperature())
    """
    ebm_model = EBM(
        num_lat=num_lat,
        water_depth=water_depth,
        S0=S0,
        A=A,
        B=B,
        D=D,
        Tf=Tf,
        ai=ai,
        **kwargs
    )
    return ebm_model
