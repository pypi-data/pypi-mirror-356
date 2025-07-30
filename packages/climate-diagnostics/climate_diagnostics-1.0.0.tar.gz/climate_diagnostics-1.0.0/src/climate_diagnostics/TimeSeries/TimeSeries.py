import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dask.diagnostics import ProgressBar
from statsmodels.tsa.seasonal import STL
from ..utils import get_coord_name, filter_by_season, get_or_create_dask_client, select_process_data, get_spatial_mean

@xr.register_dataset_accessor("climate_timeseries")
class TimeSeriesAccessor:
    """
    Accessor for analyzing and visualizing climate time series from xarray datasets.
    Provides methods for extracting, processing, and visualizing time series
    with support for weighted spatial averaging, seasonal filtering, and time series decomposition.
    """

    # --------------------------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------------------------
    def __init__(self, xarray_obj):
        """Initialize the accessor with a Dataset object."""
        self._obj = xarray_obj

    def _prepare_and_compute_timeseries(self, variable, latitude, longitude, level,
                                        time_range, season, year, area_weighted,
                                        processing_method='mean'):
        """
        Private helper to select, process, and compute a time series.
        
        This consolidates the boilerplate data handling for all public methods.
        """
        get_or_create_dask_client()
        
        # --- Step 1: Select data using the utility function ---
        data_selected = select_process_data(
            self._obj, variable, latitude, longitude, level, time_range, season, year
        )
        
        time_name = get_coord_name(data_selected, ['time', 't'])
        if not time_name or time_name not in data_selected.dims:
            raise ValueError(f"Time dimension not found in variable '{variable}'.")
        if data_selected.size == 0:
            print("Warning: No data available for the given selection.")
            return None, None

        # --- Step 2: Apply spatial processing ---
        if processing_method == 'mean':
            ts_data = get_spatial_mean(data_selected, area_weighted)
        elif processing_method == 'std':
            lat_name = get_coord_name(data_selected, ['lat', 'latitude'])
            lon_name = get_coord_name(data_selected, ['lon', 'longitude'])
            spatial_dims = [d for d in [lat_name, lon_name] if d and d in data_selected.dims]
            if not spatial_dims:
                raise ValueError("No spatial dimensions found for standard deviation calculation.")
            
            if area_weighted and lat_name in spatial_dims:
                weights = np.cos(np.deg2rad(data_selected[lat_name]))
                weights.name = "weights"
                ts_data = data_selected.weighted(weights).std(dim=spatial_dims, skipna=True)
            else:
                ts_data = data_selected.std(dim=spatial_dims, skipna=True)
        else:
            raise ValueError(f"Unknown processing method: {processing_method}")

        # --- Step 3: Trigger Dask computation ---
        if hasattr(ts_data, 'chunks') and ts_data.chunks:
            print(f"Computing time series with '{processing_method}' processing...")
            with ProgressBar():
                ts_data = ts_data.compute()
        
        if ts_data.size == 0:
            print(f"Warning: Time series is empty after spatial processing ('{processing_method}').")
            return None, None
            
        return ts_data, data_selected.attrs

    # ==============================================================================
    # PUBLIC PLOTTING METHODS
    # ==============================================================================

    # --------------------------------------------------------------------------
    # A. Basic Time Series Plots
    # --------------------------------------------------------------------------
    def plot_time_series(self, variable='air', latitude=None, longitude=None, level=None,
                         time_range=None, season='annual', year=None,
                         area_weighted=True, ax=None, figsize=(16, 10), save_plot_path=None):
        """
        Plot a time series of a spatially averaged variable.

        This function selects data for a given variable, performs spatial averaging
        over the specified domain, and plots the resulting time series.

        Parameters
        ----------
        variable : str, optional
            Name of the variable to plot. Defaults to 'air'.
        latitude : float, slice, or list, optional
            Latitude range for spatial averaging.
        longitude : float, slice, or list, optional
            Longitude range for spatial averaging.
        level : float, slice, or list, optional
            Vertical level selection.
        time_range : slice, optional
            Time range for the series.
        season : str, optional
            Seasonal filter. Defaults to 'annual'.
        year : int, optional
            Filter for a specific year.
        area_weighted : bool, optional
            If True, use latitude-based area weighting for the spatial mean. Defaults to True.
        ax : matplotlib.axes.Axes, optional
            An existing axes object to plot on. If None, a new figure is created.
        figsize : tuple, optional
            Figure size. Defaults to (16, 10).
        save_plot_path : str or None, optional
            If provided, the path to save the plot figure.

        Returns
        -------
        matplotlib.axes.Axes or None
            The Axes object of the plot, or None if no data could be plotted.
        """
        ts_data, attrs = self._prepare_and_compute_timeseries(
            variable, latitude, longitude, level, time_range, season, year, area_weighted, 'mean'
        )
        if ts_data is None:
            return None

        # --- Plotting ---
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        
        ts_data.plot(marker='.', ax=ax)

        # --- Customize plot ---
        units = attrs.get("units", "")
        long_name = attrs.get("long_name", variable.replace('_', ' ').capitalize())
        ax.set_ylabel(f"{long_name} ({units})")
        ax.set_xlabel('Time')

        season_display = season.upper() if season.lower() != 'annual' else 'Annual'
        year_display = f" for {year}" if year is not None else ""
        weight_display = "Area-Weighted " if area_weighted and 'lat' in ts_data.coords else ""
        ax.set_title(f"{season_display}{year_display}: {weight_display}Spatial Mean Time Series of {long_name}")

        ax.grid(True, linestyle='--', alpha=0.7)
        if save_plot_path:
            plt.savefig(save_plot_path, bbox_inches='tight', dpi=300)
            print(f"Plot saved to: {save_plot_path}")
        return ax

    def plot_std_space(self, variable='air', latitude=None, longitude=None, level=None,
                       time_range=None, season='annual', year=None,
                       area_weighted=True, ax=None, figsize=(16, 10), save_plot_path=None, title=None):
        """
        Plot a time series of the spatial standard deviation of a variable.

        This function calculates the standard deviation across the spatial domain
        for each time step and plots the resulting time series. This can be used
        to analyze the spatial variability of a field over time.

        Parameters
        ----------
        variable : str, optional
            Name of the variable to plot. Defaults to 'air'.
        latitude : float, slice, or list, optional
            Latitude range for the calculation.
        longitude : float, slice, or list, optional
            Longitude range for the calculation.
        level : float, slice, or list, optional
            Vertical level selection.
        time_range : slice, optional
            Time range for the series.
        season : str, optional
            Seasonal filter. Defaults to 'annual'.
        year : int, optional
            Filter for a specific year.
        area_weighted : bool, optional
            If True, use latitude-based area weighting for the standard deviation. Defaults to True.
        ax : matplotlib.axes.Axes, optional
            An existing axes object to plot on. If None, a new figure is created.
        figsize : tuple, optional
            Figure size. Defaults to (16, 10).
        save_plot_path : str or None, optional
            If provided, the path to save the plot figure.
        title : str or None, optional
            Custom plot title. A default title is generated if not provided.

        Returns
        -------
        matplotlib.axes.Axes or None
            The Axes object of the plot, or None if no data could be plotted.
        """
        std_ts_data, attrs = self._prepare_and_compute_timeseries(
            variable, latitude, longitude, level, time_range, season, year, area_weighted, 'std'
        )
        if std_ts_data is None:
            return None

        # --- Plotting ---
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            
        std_ts_data.plot(marker='.', ax=ax)

        # --- Customize plot ---
        units = attrs.get("units", "")
        long_name = attrs.get("long_name", variable.replace('_', ' ').capitalize())
        ax.set_ylabel(f"Spatial Std. Dev. ({units})" if units else "Spatial Std. Dev.")
        ax.set_xlabel('Time')

        if title is None:
            season_display = season.upper() if season.lower() != 'annual' else 'Annual'
            year_display = f" for {year}" if year is not None else ""
            weight_display = "Area-Weighted " if area_weighted else ""
            title = f"{season_display}{year_display}: Time Series of {weight_display}Spatial Std Dev of {long_name}"
        ax.set_title(title)
        
        ax.grid(True, linestyle='--', alpha=0.7)
        if save_plot_path:
            plt.savefig(save_plot_path, bbox_inches='tight', dpi=300)
            print(f"Plot saved to: {save_plot_path}")
        return ax

    # --------------------------------------------------------------------------
    # C. Time Series Decomposition
    # --------------------------------------------------------------------------
    def decompose_time_series(self, variable='air', level=None, latitude=None, longitude=None,
                              time_range=None, season='annual', year=None,
                              stl_seasonal=13, stl_period=12, area_weighted=True,
                              plot_results=True, figsize=(12, 10), save_plot_path=None):
        """
        Decompose a time series into trend, seasonal, and residual components using STL.

        Seasonal-Trend decomposition using LOESS (STL) is a robust method for
        decomposing a time series. This function first creates a spatially-averaged
        time series and then applies the STL algorithm.

        Parameters
        ----------
        variable : str, optional
            Name of the variable to decompose. Defaults to 'air'.
        level : float, slice, or list, optional
            Vertical level selection.
        latitude : float, slice, or list, optional
            Latitude range for spatial averaging.
        longitude : float, slice, or list, optional
            Longitude range for spatial averaging.
        time_range : slice, optional
            Time range for the series.
        season : str, optional
            Seasonal filter. Defaults to 'annual'.
        year : int, optional
            Filter for a specific year.
        stl_seasonal : int, optional
            Length of the seasonal smoother for STL. Must be an odd integer. Defaults to 13.
        stl_period : int, optional
            The period of the seasonal component. For monthly data, this is typically 12. Defaults to 12.
        area_weighted : bool, optional
            If True, use area weighting for the spatial mean. Defaults to True.
        plot_results : bool, optional
            If True, plot the original series and its decomposed components. Defaults to True.
        figsize : tuple, optional
            Figure size for the plot. Defaults to (12, 10).
        save_plot_path : str or None, optional
            Path to save the decomposition plot.

        Returns
        -------
        dict or (dict, matplotlib.figure.Figure)
            If `plot_results` is False, returns a dictionary containing the
            'original', 'trend', 'seasonal', and 'residual' components as pandas Series.
            If `plot_results` is True, returns a tuple of (dictionary, figure object).
        """
        ts_data, attrs = self._prepare_and_compute_timeseries(
            variable, latitude, longitude, level, time_range, season, year, area_weighted, 'mean'
        )
        if ts_data is None:
            return None
            
        # --- Convert to pandas Series for STL ---
        try:
            ts_pd = ts_data.to_series()
        except Exception:
            ts_pd = ts_data.to_pandas()
        
        if not isinstance(ts_pd, pd.Series):
            if isinstance(ts_pd, pd.DataFrame) and len(ts_pd.columns) == 1:
                ts_pd = ts_pd.iloc[:, 0]
            else:
                raise TypeError(f"Could not convert DataArray to a pandas Series. Got type: {type(ts_pd)}")
        
        # --- Apply STL decomposition ---
        if ts_pd.isnull().all():
            raise ValueError("Time series is all NaNs after selection/averaging.")
        
        ts_pd_clean = ts_pd.dropna()
        if len(ts_pd_clean) < 2 * stl_period:
            raise ValueError(
                f"Time series must contain at least 2*period (={2*stl_period}) non-NaN values "
                f"for STL decomposition, but found {len(ts_pd_clean)}."
            )

        print("Applying STL decomposition...")
        stl_result = STL(ts_pd_clean, seasonal=stl_seasonal, period=stl_period, robust=True).fit()

        # --- Plotting ---
        if plot_results:
            long_name = attrs.get("long_name", variable.replace('_', ' ').capitalize())
            units = attrs.get("units", "")
            
            fig = stl_result.plot()
            fig.set_size_inches(*figsize)
            fig.suptitle(f"STL Decomposition of {long_name} ({units})", y=1.02)
            
            if save_plot_path:
                plt.savefig(save_plot_path, bbox_inches='tight', dpi=300)
                print(f"Plot saved to: {save_plot_path}")
            plt.show()

        return stl_result

__all__ = ['TimeSeriesAccessor']
