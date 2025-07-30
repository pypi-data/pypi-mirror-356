# -*- coding: utf-8 -*-
"""
Components that require PyWake.

@author: ricriv
"""

# %% Import.


import numpy as np
import xarray as xr
from py_wake.flow_map import Points
from py_wake.utils import gradients
from py_wake.wind_farm_models.engineering_models import (
    All2AllIterative,
    PropagateDownwind,
    PropagateUpDownIterative,
)

from wind_farm_loads.tool_agnostic import (
    SmoothPotFunctions,
    _arg2ilk,
    _get_sensor_names,
    _preallocate_ilktn,
    _preallocate_sector_average,
    make_polar_grid,
    rotate_grid,
)

# %% Classes to avoid self wake and self blockage.


class PropagateDownwindNoSelfInduction(PropagateDownwind):
    """Same as `PropagateDownwind`, but the wake, added turbulence and blockage are set to 0 in a sphere that surrounds each rotor.

    The objective of this class is to obtain a flow map that does not measure
    the induction of the current turbine, while keeping the same wind farm power.
    """

    def __init__(self, *args, pot=SmoothPotFunctions.pot_sharp, **kwargs):
        PropagateDownwind.__init__(self, *args, **kwargs)
        self.pot = pot

    def _calc_deficit(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, blockage = PropagateDownwind._calc_deficit(
            self, dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight
        return deficit, blockage

    def _calc_deficit_convection(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, uc, sigma_sqr = self.wake_deficitModel.calc_deficit_convection(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        deficit, blockage = self._add_blockage(deficit, dw_ijlk, **kwargs)
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight
        return deficit, uc, sigma_sqr, blockage

    def _calc_added_turbulence(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        added_ti = self.turbulenceModel.calc_added_turbulence(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        added_ti = added_ti * weight
        return added_ti


class PropagateUpDownIterativeNoSelfInduction(PropagateUpDownIterative):
    """Same as `PropagateUpDownIterative`, but the wake, added turbulence and blockage are set to 0 in a sphere that surrounds each rotor.

    The objective of this class is to obtain a flow map that does not measure
    the induction of the current turbine, while keeping the same wind farm power.
    """

    def __init__(self, *args, pot=SmoothPotFunctions.pot_sharp, **kwargs):
        PropagateUpDownIterative.__init__(self, *args, **kwargs)
        self.pot = pot

    def _calc_deficit(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, blockage = PropagateUpDownIterative._calc_deficit(
            self, dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight

        return deficit, blockage

    def _calc_deficit_convection(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, uc, sigma_sqr = self.wake_deficitModel.calc_deficit_convection(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        deficit, blockage = self._add_blockage(deficit, dw_ijlk, **kwargs)
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight
        return deficit, uc, sigma_sqr, blockage

    def _calc_added_turbulence(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        added_ti = self.turbulenceModel.calc_added_turbulence(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        added_ti = added_ti * weight
        return added_ti


class All2AllIterativeNoSelfInduction(All2AllIterative):
    """Same as `All2AllIterative`, but the wake, added turbulence and blockage are set to 0 in a sphere that surrounds each rotor.

    The objective of this class is to obtain a flow map that does not measure
    the induction of the current turbine, while keeping the same wind farm power.
    """

    def __init__(self, *args, pot=SmoothPotFunctions.pot_sharp, **kwargs):
        All2AllIterative.__init__(self, *args, **kwargs)
        self.pot = pot

    def _calc_deficit(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, blockage = All2AllIterative._calc_deficit(
            self, dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight
        return deficit, blockage

    def _calc_deficit_convection(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        deficit, uc, sigma_sqr = self.wake_deficitModel.calc_deficit_convection(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        deficit, blockage = self._add_blockage(deficit, dw_ijlk, **kwargs)
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        deficit = deficit * weight
        if blockage is not None:
            blockage = blockage * weight
        return deficit, uc, sigma_sqr, blockage

    def _calc_added_turbulence(self, dw_ijlk, cw_ijlk, D_src_il, **kwargs):
        added_ti = self.turbulenceModel.calc_added_turbulence(
            dw_ijlk=dw_ijlk, cw_ijlk=cw_ijlk, D_src_il=D_src_il, **kwargs
        )
        r = gradients.hypot(dw_ijlk, cw_ijlk)
        weight = self.pot(r, 0.75 * D_src_il[:, np.newaxis, :, np.newaxis])
        added_ti = added_ti * weight
        return added_ti


# %% Functions to extract the inflow.


def get_rotor_averaged_wind_speed(sim_res):
    """
    Get rotor-averaged wind speed.

    Parameters
    ----------
    sim_res : py_wake SimulationResult
        A simulation result from PyWake. Must follow a call to the wind farm model.

    Returns
    -------
    WS_eff : xarray DataArray
        Effective wind speed as a function of: ambient wind speed, ambient wind direction, turbine number and type.

    """
    return sim_res["WS_eff"]


def get_rotor_averaged_turbulence_intensity(sim_res):
    """
    Get rotor-averaged turbulence intensity.

    Parameters
    ----------
    sim_res : py_wake SimulationResult
        A simulation result from PyWake. Must follow a call to the wind farm model.

    Returns
    -------
    TI_eff : xarray DataArray
        Effective turbulence intensity as a function of: ambient wind speed, ambient wind direction, turbine number and type.

    """
    return sim_res["TI_eff"]


def compute_flow_map(
    sim_res,
    x_grid,
    y_grid,
    z_grid,
    align_in_yaw=True,
    align_in_tilt=True,
    axial_wind=False,
    wt=None,
    wd=None,
    ws=None,
    time=None,
    dtype=np.float32,
    save_grid=False,
):
    r"""
    Compute the effective wind speed and Turbulence Intensity over a rotor.

    This function receives a grid, and then rotates it by the wind direction. Optionally,
    the grid is also rotated by the yaw and tilt of each turbine to align it with the rotor plane.
    Finally, the grid is translated to each rotor center and the flow map is computed.

    Parameters
    ----------
    sim_res : py_wake SimulationResult
        Simulation result computed by PyWake. Must follow a call to the wind farm model.
    x_grid : (N, M) or (N, M, Type) ndarray
        x coordinate (downwind) of the grid points, before rotation by yaw and tilt. Should be 0.
        Typically generated by `make_rectangular_grid` or `make_polar_grid`.
        The first 2 dimensions cover the rotor, while the last is over the turbine types.
        If the user passes a 2D array, the grid is assumed to be the same for all turbine types.
    y_grid : (N, M) or (N, M, Type) ndarray
        List of y coordinate (crosswind) of the grid points, before rotation by yaw and tilt.
        Typically generated by `make_rectangular_grid` or `make_polar_grid`.
        If the user passes a 2D array, the grid is assumed to be the same for all turbine types.
    z_grid : (N, M) or (N, M, Type) ndarray
        List of z coordinate (up) of the grid points, before rotation by yaw and tilt.
        Typically generated by `make_rectangular_grid` or `make_polar_grid`.
        If the user passes a 2D array, the grid is assumed to be the same for all turbine types.
    align_in_yaw : bool, optional
        If `True` (default) the grid is aligned in yaw with the rotor plane.
    align_in_tilt : bool, optional
        If `True` (default) the grid is aligned in tilt with the rotor plane.
    axial_wind : bool, optional
        If `True` the axial wind speed and TI are returned. That is, the downstream wind speed computed by PyWake
        is multiplied by :math:`\cos(\mathrm{yaw}) \cos(\mathrm{tilt})`. The default is `False`.
    wt : int, (I) array_like, optional
        Wind turbines. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind turbines.
    wd : float, (L) array_like, optional
        Wind direction, in deg. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind directions.
    ws : float, (K) array_like, optional
        Wind speed. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind speeds.
    time : float, (Time) array_like, optional
        Time. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available time instants.
    dtype : data-type, optional
        The desired data-type for the result. The default is single precision,
        which should be enough for all outputs. The properties of each type can
        be checked with `np.finfo(np.float32(1.0))`.
    save_grid : bool, optional
        If `True` the grid will be saved for all inflow conditions. Since this comes at a significant
        memory cost, it is recommended to switch it on only for debug purposes.
        The default is `False`.

    Returns
    -------
    flow_map : xarray DataSet
        Effective wind speed, effective turbulence intensity and corresponding grid points
        for each turbine and flow case.

    """
    # Get the number of turbine types.
    n_types = len(sim_res.windFarmModel.windTurbines._names)

    # The grid must be a numpy array with 3 dimensions.
    # The first 2 cover the rotor, while the last is over the types.
    # This implies that all turbine types must have the same number of grid points.
    # If the user passes a 2D array, the grid is assumed to be the same for all types.
    if x_grid.ndim == 2 and y_grid.ndim == 2 and z_grid.ndim == 2:
        x_grid_t = np.broadcast_to(
            x_grid[:, :, np.newaxis], (x_grid.shape[0], x_grid.shape[1], n_types)
        )
        y_grid_t = np.broadcast_to(
            y_grid[:, :, np.newaxis], (y_grid.shape[0], y_grid.shape[1], n_types)
        )
        z_grid_t = np.broadcast_to(
            z_grid[:, :, np.newaxis], (z_grid.shape[0], z_grid.shape[1], n_types)
        )

    elif x_grid.ndim == 3 and y_grid.ndim == 3 and z_grid.ndim == 3:
        x_grid_t = x_grid
        y_grid_t = y_grid
        z_grid_t = z_grid
        # Check that there is 1 grid per turbine type.
        if x_grid_t.shape[2] != n_types:
            raise ValueError(
                f"{x_grid_t.shape[2]} grid types provided, but {n_types} were expected."
            )
    else:
        raise ValueError("The grid must be a 2D or 3D array.")

    # The default value of wt, wd, ws and time is the one in sim_res.
    wt_ = sim_res["wt"].values if wt is None else np.atleast_1d(wt)
    wd_ = sim_res["wd"].values if wd is None else np.atleast_1d(wd)
    ws_ = sim_res["ws"].values if ws is None else np.atleast_1d(ws)
    if "time" in sim_res.dims:
        time_ = sim_res["time"].values if time is None else np.atleast_1d(time)

    # Convert yaw and tilt to arrays.
    # If time is not present the result has shape (I, L, K), i.e. (turbines, wind directions, wind speeds).
    # Instead, if time is present, the result has shape (I, Time), i.e. (turbines, time).
    # These arrays are contained in sim_res, therefore all turbines, directions and speeds and times must be used.
    I = sim_res.sizes["wt"]
    if "time" in sim_res.dims:
        Time = sim_res.sizes["time"]
        if align_in_yaw:
            yaw_turbines_ = _arg2ilk("yaw", sim_res["yaw"].values, I, Time)
        else:
            yaw_turbines_ = _arg2ilk("yaw", 0.0, I, Time)
        if align_in_tilt:
            tilt_turbines_ = _arg2ilk("tilt", sim_res["tilt"].values, I, Time)
        else:
            tilt_turbines_ = _arg2ilk("tilt", 0.0, I, Time)
    else:
        L = sim_res.sizes["wd"]
        K = sim_res.sizes["ws"]
        if align_in_yaw:
            yaw_turbines_ = _arg2ilk("yaw", sim_res["yaw"].values, I, L, K)
        else:
            yaw_turbines_ = _arg2ilk("yaw", 0.0, I, L, K)
        if align_in_tilt:
            tilt_turbines_ = _arg2ilk("tilt", sim_res["tilt"].values, I, L, K)
        else:
            tilt_turbines_ = _arg2ilk("tilt", 0.0, I, L, K)

    # Conveniently access turbine position.
    x_turbines_ = sim_res["x"].values
    y_turbines_ = sim_res["y"].values
    z_turbines_ = sim_res["h"].values

    # Preallocate DataSet for effective wind speed, turbulence intensity and grid points.
    # In the flow map computed by PyWake the order of dimensions is: points (1D), wd, ws, or points (1D), time.
    # In the flow map returned by this function wt, wd and ws, or time, are placed first, followed by the quantity and grid dimensions.
    # This order enables vectorization in predict_loads_pod().
    # Each turbine type is allowed to have a different grid, but all grids must have the same number of points.
    # The grid dimensions are labeled q0 and q1 because they might either be y and z or radius and azimuth.
    xr_dict = {}
    if "time" in sim_res.dims:
        # Set the independent coordinates: turbine, time and quantity.
        coords_flow = {
            "wt": wt_,
            "time": time_,
            "quantity": ["WS_eff", "TI_eff"],
        }
        dims_flow = list(coords_flow) + ["q0", "q1"]
        # Set the dependent coordinates: wind direction and wind speed.
        time_index = np.searchsorted(sim_res["time"].values, time_)
        coords_flow["wd"] = (["time"], wd_[time_index])
        coords_flow["ws"] = (["time"], ws_[time_index])

        xr_dict["flow"] = xr.DataArray(
            data=np.full(
                (
                    wt_.size,
                    time_.size,
                    2,  # Effective wind speed and TI.
                    x_grid_t.shape[0],
                    x_grid_t.shape[1],
                ),
                np.nan,
                dtype=dtype,
            ),
            coords=coords_flow,
            dims=dims_flow,
        )

        if save_grid:
            xr_dict["grid"] = xr.DataArray(
                data=np.full(
                    (
                        wt_.size,
                        time_.size,
                        3,  # x, y, z
                        x_grid_t.shape[0],
                        x_grid_t.shape[1],
                    ),
                    np.nan,
                    dtype=dtype,
                ),
                coords={
                    "wt": wt_,
                    "time": time_,
                    "axis": ["x", "y", "z"],
                },
                dims=["wt", "time", "axis", "q0", "q1"],
            )

    else:  # "time" not in sim_res.dims
        xr_dict["flow"] = xr.DataArray(
            data=np.full(
                (
                    wt_.size,
                    wd_.size,
                    ws_.size,
                    2,  # Effective wind speed and TI.
                    x_grid_t.shape[0],
                    x_grid_t.shape[1],
                ),
                np.nan,
                dtype=dtype,
            ),
            coords={
                "wt": wt_,
                "wd": wd_,
                "ws": ws_,
                "quantity": ["WS_eff", "TI_eff"],
            },
            dims=["wt", "wd", "ws", "quantity", "q0", "q1"],
        )

        if save_grid:
            xr_dict["grid"] = xr.DataArray(
                data=np.full(
                    (
                        wt_.size,
                        wd_.size,
                        ws_.size,
                        3,  # x, y, z
                        x_grid_t.shape[0],
                        x_grid_t.shape[1],
                    ),
                    np.nan,
                    dtype=dtype,
                ),
                coords={
                    "wt": wt_,
                    "wd": wd_,
                    "ws": ws_,
                    "axis": ["x", "y", "z"],
                },
                dims=["wt", "wd", "ws", "axis", "q0", "q1"],
            )
    ds = xr.Dataset(xr_dict)

    # Convert all angles from deg to rad.
    wd_rad = np.deg2rad(wd_)
    yaw_turbines_ = np.deg2rad(yaw_turbines_)
    tilt_turbines_ = np.deg2rad(tilt_turbines_)

    cos_yaw_cos_tilt = np.cos(yaw_turbines_) * np.cos(tilt_turbines_)

    angle_ref = np.deg2rad(90.0)

    if "time" in sim_res.dims:
        # Loop over the turbines.
        for i in wt_:
            # Get type of current turbine.
            i_type = int(sim_res["type"][i])
            # Loop over time.
            for t in range(time_.size):
                # Convert grid from downwind-crosswind-z to east-north-z.
                # While doing that, also rotate by yaw and tilt.
                # This can be done because the order of rotations is first yaw and then tilt.
                # It will NOT work for a floating turbine.
                # We rely on this function to create new arrays, so that the following
                # translation will not affect the original ones.
                # The formula for the yaw is taken from py_wake.wind_turbines._wind_turbines.WindTurbines.plot_xy()
                x_grid_, y_grid_, z_grid_ = rotate_grid(
                    x_grid_t[:, :, i_type],
                    y_grid_t[:, :, i_type],
                    z_grid_t[:, :, i_type],
                    yaw=angle_ref - wd_rad[t] + yaw_turbines_[i, t],  # [rad]
                    tilt=-tilt_turbines_[i, t],  # [rad]
                    degrees=False,
                )
                # Move grid to rotor center. The turbine position is in east-north-z coordinates.
                x_grid_ += x_turbines_[i]
                y_grid_ += y_turbines_[i]
                z_grid_ += z_turbines_[i]
                it = {"wt": wt_[i], "time": time_[t]}
                if save_grid:
                    ds["grid"].loc[{**it, "axis": "x"}] = x_grid_
                    ds["grid"].loc[{**it, "axis": "y"}] = y_grid_
                    ds["grid"].loc[{**it, "axis": "z"}] = z_grid_
                # Compute flow map.
                flow_map = sim_res.flow_map(
                    grid=Points(x_grid_.ravel(), y_grid_.ravel(), z_grid_.ravel()),
                    time=[time_[t]],
                )
                ds["flow"].loc[{**it, "quantity": "WS_eff"}] = flow_map[
                    "WS_eff"
                ].values.reshape(x_grid_.shape)
                ds["flow"].loc[{**it, "quantity": "TI_eff"}] = flow_map[
                    "TI_eff"
                ].values.reshape(x_grid_.shape)

        # Project wind speed.
        if axial_wind:
            ds["flow"] *= cos_yaw_cos_tilt[:, :, np.newaxis, np.newaxis, np.newaxis]

    else:  # "time" not in sim_res.dims
        # Loop over the turbines.
        for i in wt_:
            # Get type of current turbine.
            i_type = int(sim_res["type"][i])
            # Loop over wind directions.
            for l in range(wd_.size):
                # Loop over wind speeds.
                for k in range(ws_.size):
                    # Convert grid from downwind-crosswind-z to east-north-z.
                    # While doing that, also rotate by yaw and tilt.
                    # This can be done because the order of rotations is first yaw and then tilt.
                    # It will NOT work for a floating turbine.
                    # We rely on this function to create new arrays, so that the following
                    # translation will not affect the original ones.
                    # The formula for the yaw is taken from py_wake.wind_turbines._wind_turbines.WindTurbines.plot_xy()
                    x_grid_, y_grid_, z_grid_ = rotate_grid(
                        x_grid_t[:, :, i_type],
                        y_grid_t[:, :, i_type],
                        z_grid_t[:, :, i_type],
                        yaw=angle_ref - wd_rad[l] + yaw_turbines_[i, l, k],  # [rad]
                        tilt=-tilt_turbines_[i, l, k],  # [rad]
                        degrees=False,
                    )
                    # Move grid to rotor center. The turbine position is in east-north-z coordinates.
                    x_grid_ += x_turbines_[i]
                    y_grid_ += y_turbines_[i]
                    z_grid_ += z_turbines_[i]
                    ilk = {"wt": wt_[i], "wd": wd_[l], "ws": ws_[k]}
                    if save_grid:
                        ds["grid"].loc[{**ilk, "axis": "x"}] = x_grid_
                        ds["grid"].loc[{**ilk, "axis": "y"}] = y_grid_
                        ds["grid"].loc[{**ilk, "axis": "z"}] = z_grid_
                    # Compute flow map.
                    flow_map = sim_res.flow_map(
                        grid=Points(x_grid_.ravel(), y_grid_.ravel(), z_grid_.ravel()),
                        wd=wd_[l],
                        ws=ws_[k],
                    )
                    ds["flow"].loc[{**ilk, "quantity": "WS_eff"}] = flow_map[
                        "WS_eff"
                    ].values.reshape(x_grid_.shape)
                    ds["flow"].loc[{**ilk, "quantity": "TI_eff"}] = flow_map[
                        "TI_eff"
                    ].values.reshape(x_grid_.shape)

        # Project wind speed.
        if axial_wind:
            ds["flow"] *= cos_yaw_cos_tilt[:, :, :, np.newaxis, np.newaxis, np.newaxis]

    return ds


def compute_sector_average(
    sim_res,
    n_radius=100,
    n_azimuth=181,
    look="downwind",
    axial_wind=False,
    wt=None,
    wd=None,
    ws=None,
    time=None,
    dtype=np.float32,
):
    """
    Compute the sector-averaged effective wind speed and effective turbulence intensity, assuming 4 sectors.

    Each sector spans 90 deg in azimuth and they are oriented as left, up, right and down, as
    described in `Guilloré, A., Campagnolo, F. & Bottasso, C. L. (2024). A control-oriented load surrogate model based on sector-averaged inflow quantities: capturing damage for unwaked, waked, wake-steering and curtailed wind turbines <https://doi.org/10.1088/1742-6596/2767/3/032019>`_

    The result can be visualized via `wind_farm_loads.tool_agnostic.plot_sector_average()`.

    Parameters
    ----------
    sim_res : py_wake SimulationResult
        Simulation result computed by PyWake. Must follow a call to the wind farm model.
    n_radius : int, optional
        Number of points along the rotor radius. The default is 100.
    n_azimuth : int, optional
        Number of points along the rotor azimuth. Must be odd.
        The default is 181, which ensures 2 deg per azimuth step.
    look : str, optional
        The left and right sectors are determined by an observer that can look
        `"upwind"` or `"downwind"`. The default is `"downwind"`.
    axial_wind : bool, optional
        If `True` the axial wind speed and TI are returned. The default is `False`.
    wt : int, (I) array_like, optional
        Wind turbines. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind turbines.
    wd : float, (L) array_like, optional
        Wind direction, in deg. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind directions.
    ws : float, (K) array_like, optional
        Wind speed. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available wind speeds.
    time : float, (Time) array_like, optional
        Time. Must be a subset of the one contained in `sim_res`.
        The default is `None`, which means to use all available time instants.
    dtype : data-type, optional
        The desired data-type for the result. The default is single precision,
        which should be enough for all outputs. The properties of each type can
        be checked with `np.finfo(np.float32(1.0))`.

    Returns
    -------
    sa : xarray DataArray
        Sector-averaged wind speed, effective turbulence intensity for each turbine and flow case.

    """
    # Check that n_azimuth is odd.
    assert n_azimuth % 2 == 1

    # Make the azimuth grid. We cover 360 deg starting from -45, which is the
    # beginning of the left sector.
    # We also add 1 more point at the end for easier slicing later on.
    dazim = 360.0 / (n_azimuth - 1)  # Azimuth step.
    azimuth = np.linspace(-45.0, 360.0 - 45.0 + dazim, n_azimuth + 1, endpoint=True)

    # Make the polar grid for each turbine type.
    diameters = sim_res.windFarmModel.windTurbines._diameters
    n_types = len(diameters)
    x_grid = np.zeros((n_radius, n_azimuth + 1, n_types))
    y_grid = np.zeros((n_radius, n_azimuth + 1, n_types))
    z_grid = np.zeros((n_radius, n_azimuth + 1, n_types))
    for i in range(n_types):
        radius = np.linspace(0.0, 0.5 * diameters[i], n_radius)
        x_grid[:, :, i], y_grid[:, :, i], z_grid[:, :, i] = make_polar_grid(
            radius, azimuth, degrees=True
        )

    # Get the flow map.
    flow_map = compute_flow_map(
        sim_res,
        x_grid,
        y_grid,
        z_grid,
        axial_wind=axial_wind,
        wt=wt,
        wd=wd,
        ws=ws,
        time=time,
        dtype=dtype,
    )
    # Compute the sector average.
    sa = _preallocate_sector_average(
        wt=flow_map["wt"].values,
        wd=flow_map["wd"].values,
        ws=flow_map["ws"].values,
        time=flow_map["time"].values if "time" in flow_map.dims else None,
        dtype=dtype,
    )

    # Number of azimuth steps in each sector.
    i_sector_size = (n_azimuth - 1) // 4
    # Compute the sector average for the up and down sectors.
    # q0 is radius and q1 is azimuth.
    sa.loc[{"direction": "up"}] = flow_map["flow"][
        ..., i_sector_size : 2 * i_sector_size
    ].mean(dim=["q0", "q1"])
    sa.loc[{"direction": "down"}] = flow_map["flow"][
        ..., 3 * i_sector_size : n_azimuth
    ].mean(dim=["q0", "q1"])

    # Compute the sector average for the left and right sectors.
    if look == "upwind":
        sa.loc[{"direction": "left"}] = flow_map["flow"][..., 0:i_sector_size].mean(
            dim=["q0", "q1"]
        )
        sa.loc[{"direction": "right"}] = flow_map["flow"][
            ..., 2 * i_sector_size : 3 * i_sector_size
        ].mean(dim=["q0", "q1"])

    elif look == "downwind":
        sa.loc[{"direction": "right"}] = flow_map["flow"][..., 0:i_sector_size].mean(
            dim=["q0", "q1"]
        )
        sa.loc[{"direction": "left"}] = flow_map["flow"][
            ..., 2 * i_sector_size : 3 * i_sector_size
        ].mean(dim=["q0", "q1"])

    else:
        raise ValueError("Parameter look must be 'upwind' or 'downwind'")

    return sa


# %% Functions to evaluate the loads.


def predict_loads_rotor_average(
    surrogates, sim_res, *additional_inputs, dtype=np.float32, ti_in_percent=True
):
    r"""
    Evaluate the load surrogate models based on rotor-averaged wind speed and turbulence intensity. Additional (control) inputs are supported as well.

    Each load surrogate is evaluated as

    .. math::
      y = f(\mathrm{WS}, \mathrm{TI}, \boldsymbol{\theta})

    where :math:`\mathrm{WS}` is the rotor-averaged wind speed, :math:`\mathrm{TI}` is the rotor-averaged turbulence intensity and
    :math:`\boldsymbol{\theta}` are the additional inputs (typically, control parameters). The surrogates are evaluated
    for all turbines and ambient inflow conditions.

    The load database has been described in
    `Guilloré, A., Campagnolo, F. & Bottasso, C. L. (2024). A control-oriented load surrogate model based on sector-averaged inflow quantities: capturing damage for unwaked, waked, wake-steering and curtailed wind turbines <https://doi.org/10.1088/1742-6596/2767/3/032019>`_
    where it was proposed to include the controller set point by adding the yaw, pitch and rotor speed.
    This function has been developed using the surrogate models trained by Hari, which are based on the database provided by TUM.

    Parameters
    ----------
    surrogates : dict of surrogates_interface.surrogates.SurrogateModel
        Dictionary containing surrogate models. The keys will be used as sensor names.
    sim_res : py_wake SimulationResult
        Simulation result computed by PyWake. Must follow a call to the wind farm model.
    additional_inputs : list of ndarray
        Additional inputs to evaluate the load surrogate models.
        Must be coherent with the simulation result. PyWake rules are applied to broadcast each additional
        input to shape `(wt, wd, ws)` or `(wt, time)`. Typical additional inputs are:

            - Yaw, pitch and rotor speed.
            - Yaw and curtailment level.

        It is the user responsibility to pass the inputs in the order required by the surrogates, and to use the correct units.
    dtype : data-type, optional
        The desired data-type for the result. The default is single precision,
        which should be enough for all outputs. The properties of each type can
        be checked with `np.finfo(np.float32(1.0))`.
    ti_in_percent : bool
        If `True` (default) the turbulence intensity is multiplied by 100 before evaluating the surrogates.

    Returns
    -------
    loads : xarray.DataArray
        Loads for each turbine, ambient inflow condition and sensor.

    """
    # Preallocate a DataArray for the results.
    loads = _preallocate_ilktn(
        wt=sim_res["wt"].values,
        wd=sim_res["wd"].values,
        ws=sim_res["ws"].values,
        time=sim_res["time"].values if "time" in sim_res.dims else None,
        name=_get_sensor_names(surrogates),
        dtype=dtype,
    )

    # Multiply the turbulence intensity by 100?
    if ti_in_percent:
        ti = sim_res["TI_eff"].values.ravel() * 100.0
    else:
        ti = sim_res["TI_eff"].values.ravel()

    # Ensure that the additional inputs have shape [wt, wd, ws] or [wt, time].
    theta = []
    if "time" in sim_res.dims:
        theta = [
            _arg2ilk("additional_input", th, sim_res["wt"].size, sim_res["time"].size)
            .astype(dtype)
            .ravel()
            for th in additional_inputs
        ]
    else:
        theta = [
            _arg2ilk(
                "additional_input",
                th,
                sim_res["wt"].size,
                sim_res["wd"].size,
                sim_res["ws"].size,
            )
            .astype(dtype)
            .ravel()
            for th in additional_inputs
        ]

    # Compose input for load surrogate.
    x = np.column_stack(
        (
            sim_res["WS_eff"].values.astype(dtype).ravel(),  # [m/s]
            ti.astype(dtype),
            *theta,
        )
    )

    # Loop over the surrogate models and evaluate them.
    for sensor in surrogates.keys():
        loads.loc[{"name": sensor}] = (
            surrogates[sensor].predict_output(x).reshape(sim_res["WS_eff"].shape)
        )
    return loads


def predict_loads_pod(
    surrogates,
    sim_res,
    flow_map,
    *additional_inputs,
    dtype=np.float32,
    ti_in_percent=True,
):
    r"""
    Evaluate the load surrogate models based on Proper Orthogonal Decomposition of wind speed and turbulence intensity. Additional (control) inputs are supported as well.

    Each load surrogate is evaluated as

    .. math::
      y = f(\mathrm{WS}, \mathrm{TI}, \boldsymbol{\theta})

    where :math:`\mathrm{WS}` is the wind speed over the grid used to generated the POD basis, :math:`\mathrm{TI}` is
    the turbulence intensity over the grid used to generated the POD basis and :math:`\boldsymbol{\theta}` are the
    additional inputs (typically, control parameters). The surrogates are evaluated for all turbines and ambient inflow conditions.

    The load database has been described in
    `Guilloré, A., Campagnolo, F. & Bottasso, C. L. (2024). A control-oriented load surrogate model based on sector-averaged inflow quantities: capturing damage for unwaked, waked, wake-steering and curtailed wind turbines <https://doi.org/10.1088/1742-6596/2767/3/032019>`_
    where it was proposed to include the controller set point by adding the yaw, pitch and rotor speed.
    This function has been developed using the surrogate models trained by Hari, which are based on the database provided by TUM.

    Parameters
    ----------
    surrogates : dict of surrogates_interface.surrogates.SurrogateModel
        Dictionary containing surrogate models. The keys will be used as sensor names.
    sim_res : py_wake SimulationResult
        Simulation result computed by PyWake. Must follow a call to the wind farm model.
    flow_map : xarray DataSet
        Effective wind speed, effective turbulence intensity and corresponding grid points
        for each turbine and flow case. Generated by `compute_flow_map()`.
    additional_inputs : list of ndarray
        Additional inputs to evaluate the load surrogate models.
        Must be coherent with the simulation result. PyWake rules are applied to broadcast each additional
        input to shape `(wt, wd, ws)` or `(wt, time)`. Typical additional inputs are:

            - Yaw, pitch and rotor speed.
            - Yaw and curtailment level.

        It is the user responsibility to pass the inputs in the order required by the surrogates, and to use the correct units.
    dtype : data-type, optional
        The desired data-type for the result. The default is single precision,
        which should be enough for all outputs. The properties of each type can
        be checked with `np.finfo(np.float32(1.0))`.
    ti_in_percent : bool
        If `True` (default) the turbulence intensity is multiplied by 100 before evaluating the surrogates.

    Returns
    -------
    loads : xarray.DataArray
        Loads for each turbine, ambient inflow condition and sensor.

    """
    # Preallocate a DataArray for the results.
    loads = _preallocate_ilktn(
        wt=flow_map["wt"].values,
        wd=flow_map["wd"].values,
        ws=flow_map["ws"].values,
        time=flow_map["time"].values if "time" in flow_map.dims else None,
        name=_get_sensor_names(surrogates),
        dtype=dtype,
    )

    # Multiply the turbulence intensity by 100?
    if ti_in_percent:
        ti = flow_map["flow"].loc[{"quantity": "TI_eff"}].values * 100.0
    else:
        ti = flow_map["flow"].loc[{"quantity": "TI_eff"}].values

    # Ensure that the additional inputs have shape (wt, wd, ws) or (wt, time).
    # Then reshape to column array.
    # We take the sizes from the flow map, rather than sim_res, because the flow map
    # might contain a subset of it.
    theta = []
    if "time" in sim_res.dims:
        theta = [
            _arg2ilk("additional_input", th, flow_map["wt"].size, flow_map["time"].size)
            .astype(dtype)
            .reshape(-1, 1)
            for th in additional_inputs
        ]
    else:
        theta = [
            _arg2ilk(
                "additional_input",
                th,
                flow_map["wt"].size,
                flow_map["wd"].size,
                flow_map["ws"].size,
            )
            .astype(dtype)
            .reshape(-1, 1)
            for th in additional_inputs
        ]

    # Compose input for load surrogate.
    # We want points on the rows and features on the columns, hence the reshape.
    # Points are: wt, wd and ws or wt and time.
    # Features are: WS, TI and additional inputs.
    if "time" in sim_res.dims:
        shape_flow = (
            flow_map["wt"].size * flow_map["time"].size,
            1  # 1 because each quantity (WS and TI) is kept separate.
            * flow_map["q0"].size
            * flow_map["q1"].size,
        )
        shape_load = (flow_map["wt"].size, flow_map["time"].size)
    else:
        shape_flow = (
            flow_map["wt"].size * flow_map["wd"].size * flow_map["ws"].size,
            1  # 1 because each quantity (WS and TI) is kept separate.
            * flow_map["q0"].size
            * flow_map["q1"].size,
        )
        shape_load = (flow_map["wt"].size, flow_map["wd"].size, flow_map["ws"].size)
    x = np.concatenate(
        (
            flow_map["flow"]
            .loc[{"quantity": "WS_eff"}]
            .values.astype(dtype)
            .reshape(shape_flow),
            ti.astype(dtype).reshape(shape_flow),
            *theta,
        ),
        axis=1,
    )

    # Evaluate loads.
    for sensor in list(surrogates.keys()):
        loads.loc[{"name": sensor}] = (
            surrogates[sensor].predict_output(x).reshape(shape_load)
        )

    return loads


def predict_loads_sector_average(
    surrogates,
    sim_res,
    sector_average,
    *additional_inputs,
    dtype=np.float32,
    ti_in_percent=True,
):
    r"""
    Evaluate the load surrogate models based on sector average of wind speed and turbulence intensity. Additional (control) inputs are supported as well.

    Each load surrogate is evaluated as

    .. math::
      y = f(\mathrm{WS}, \mathrm{TI}, \boldsymbol{\theta})

    where :math:`\mathrm{WS}` is the sector-averaged wind speed, :math:`\mathrm{TI}` is the sector-averaged
    turbulence intensity and :math:`\boldsymbol{\theta}` are the additional inputs (typically, control parameters).
    The surrogates are evaluated for all turbines and ambient inflow conditions.

    The load database has been described in
    `Guilloré, A., Campagnolo, F. & Bottasso, C. L. (2024). A control-oriented load surrogate model based on sector-averaged inflow quantities: capturing damage for unwaked, waked, wake-steering and curtailed wind turbines <https://doi.org/10.1088/1742-6596/2767/3/032019>`_
    where it was proposed to include the controller set point by adding the yaw, pitch and rotor speed.
    This function has been developed using the surrogate models trained by Hari, which are based on the database provided by TUM.

    Parameters
    ----------
    surrogates : dict of surrogates_interface.surrogates.SurrogateModel
        Dictionary containing surrogate models. The keys will be used as sensor names.
    sim_res : py_wake SimulationResult
        Simulation result computed by PyWake. Must follow a call to the wind farm model.
    sector_average : xarray DataArray
        Sector average of effective wind speed and effective turbulence intensity
        for each turbine and flow case. Generated by `compute_sector_average()`.
    additional_inputs : list of ndarray
        Additional inputs to evaluate the load surrogate models.
        Must be coherent with the simulation result. PyWake rules are applied to broadcast each additional
        input to shape `(wt, wd, ws)` or `(wt, time)`. Typical additional inputs are:

            - Yaw, pitch and rotor speed.
            - Yaw and curtailment level.

        It is the user responsibility to pass the inputs in the order required by the surrogates, and to use the correct units.
    dtype : data-type, optional
        The desired data-type for the result. The default is single precision,
        which should be enough for all outputs. The properties of each type can
        be checked with `np.finfo(np.float32(1.0))`.
    ti_in_percent : bool
        If `True` (default) the turbulence intensity is multiplied by 100 before evaluating the surrogates.

    Returns
    -------
    loads : xarray.DataArray
        Loads for each turbine, ambient inflow condition and sensor.

    """
    # Preallocate a DataArray for the results.
    loads = _preallocate_ilktn(
        wt=sector_average["wt"].values,
        wd=sector_average["wd"].values,
        ws=sector_average["ws"].values,
        time=sector_average["time"].values if "time" in sector_average.dims else None,
        name=_get_sensor_names(surrogates),
        dtype=dtype,
    )

    # Multiply the turbulence intensity by 100?
    if ti_in_percent:
        ti = sector_average.loc[{"quantity": "TI_eff"}].values * 100.0
    else:
        ti = sector_average.loc[{"quantity": "TI_eff"}].values

    # Ensure that the additional inputs have shape (wt, wd, ws) or (wt, time).
    # Then reshape to column array.
    # We take the sizes from the flow map, rather than sim_res, because the flow map
    # might contain a subset of it.
    theta = []
    if "time" in sim_res.dims:
        theta = [
            _arg2ilk(
                "additional_input",
                th,
                sector_average["wt"].size,
                sector_average["time"].size,
            )
            .astype(dtype)
            .reshape(-1, 1)
            for th in additional_inputs
        ]
        shape_load = (
            sector_average["wt"].size,
            sector_average["time"].size,
        )
    else:
        theta = [
            _arg2ilk(
                "additional_input",
                th,
                sector_average["wt"].size,
                sector_average["wd"].size,
                sector_average["ws"].size,
            )
            .astype(dtype)
            .reshape(-1, 1)
            for th in additional_inputs
        ]
        shape_load = (
            sector_average["wt"].size,
            sector_average["wd"].size,
            sector_average["ws"].size,
        )

    # Compose input for load surrogate.
    # We want points on the rows and features on the columns, hence the reshape.
    # Points are: wt, wd and ws or wt and time.
    # Features are: sector-averaged WS, sector-averaged TI and additional inputs.
    # Assumes that the order of the sectors matches the one of the surrogate.
    # In this case, the sectors must be ordered as: up, right, down and left.
    n_sectors = sector_average["direction"].size
    x = np.concatenate(
        (
            sector_average.loc[{"quantity": "WS_eff"}]
            .values.astype(dtype)
            .reshape((-1, n_sectors)),
            ti.astype(dtype).reshape((-1, n_sectors)),
            *theta,
        ),
        axis=1,
    )

    # Evaluate loads.
    for sensor in list(surrogates.keys()):
        loads.loc[{"name": sensor}] = (
            surrogates[sensor].predict_output(x).reshape(shape_load)
        )

    return loads
