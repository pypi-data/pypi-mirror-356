from climlab.model.ebm import EBM
from climlab.radiation import Boltzmann

def create_boltzmann_ebm_model(
    eps=0.65,
    num_lat=90,
    water_depth=10.0,
    S0=1365.2,
    D=0.555,
    Tf=-10.0,
    ai=0.62,
    **kwargs
):
    """
    Creates a latitudinally-dependent EBM using the Stefan-Boltzmann law for OLR.

    This function initializes the standard `climlab.EBM` and then replaces its
    default linearized longwave radiation component (`A+BT`) with the more
    fundamental `climlab.radiation.Boltzmann` process.

    Parameters
    ----------
    eps : float, optional
        The longwave emissivity of the surface. Defaults to 0.65.
    num_lat : int, optional
        Number of latitude bands. Defaults to 90.
    water_depth : float, optional
        Depth of the ocean mixed layer in meters. Defaults to 10.0.
    S0 : float, optional
        The solar constant in W/m^2. Defaults to 1365.2.
    D : float, optional
        The meridional heat diffusion coefficient in W/m^2/K. Defaults to 0.555.
    Tf : float, optional
        The freezing temperature in °C for albedo calculations. Defaults to -10.0.
    ai : float, optional
        The albedo of an ice-covered surface. Defaults to 0.62.
    **kwargs : dict
        Additional keyword arguments passed to the `climlab.EBM` constructor.

    Returns
    -------
    climlab.model.ebm.EBM
        An initialized `climlab` EBM process configured with Boltzmann
        longwave radiation, ready for integration.
    """
    # Create a standard EBM, passing through relevant parameters.
    # A and B are ignored as the LW component is being replaced.
    ebm_model = EBM(
        num_lat=num_lat,
        water_depth=water_depth,
        S0=S0,
        D=D,
        Tf=Tf,
        ai=ai,
        **kwargs
    )

    # Create and add the new Boltzmann longwave radiation subprocess
    boltzmann_lw = Boltzmann(state=ebm_model.state, eps=eps)
    ebm_model.remove_subprocess('LW')
    ebm_model.add_subprocess('LW', boltzmann_lw)

    return ebm_model
