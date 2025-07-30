import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import warnings
from .math_utils import derivative_FDM

def conduction_radial_steady_numerical(r, L, bc, k, gridpoints, solver="RK45", tol=1e-3):
    """
    Solve steady-state radial heat conduction in a cylinder numerically with possible temperature-dependent thermal conductivity.

    Parameters
    ----------
    r : tuple of floats
        Radial domain as (r0, R), inner and outer radii.
    L : float
        Axial length of the cylinder (used to calculate cylindrical surface area).
    bc : tuple
        Boundary conditions at r0 as (T0, T1_input, Q):
        - T0: Temperature at inner radius r0.
        - T1_input: Temperature gradient dT/dr at r0 (can be None if unknown).
        - Q: Heat flux at r0 (can be None if unknown).
        Exactly one of T1_input or Q must be provided, or both must be consistent.
    k : float or array-like
        Thermal conductivity. Can be:
        - A constant float or int.
        - An array-like [[T0, k0], [T1, k1], ...] specifying temperature-dependent conductivity,
          which is interpolated internally.
    gridpoints : int
        Number of points in radial mesh for numerical solution.
    solver : str, optional
        ODE solver method for scipy.integrate.solve_ivp (default "RK45").
    tol : float, optional
        Relative tolerance for heat flux conservation check (default 1e-3).

    Returns
    -------
    dict
        Dictionary containing:
        - 'r': radial positions array,
        - 'T': temperature distribution array,
        - 'dT/dr': temperature gradient array,
        - 'Q_error': difference between heat flux at inner and outer boundaries (flux conservation error).

    Description
    -----------
    Solves the nonlinear ODE system describing steady radial heat conduction in a cylinder:

        d/dr [k(T) * A(r) * dT/dr] = 0,

    where A(r) = 2 * pi * r * L is the cylindrical surface area.

    The equation expands to:

        d²T/dr² + (1/k) * (dk/dT) * (dT/dr)² + (1/r) * dT/dr = 0,

    with boundary conditions at the inner radius r0:

        T(r0) = T0,
        and either specified temperature gradient dT/dr(r0) = T1_input
        or specified heat flux Q = -k * A(r0) * dT/dr(r0).

    The function supports temperature-dependent thermal conductivity via interpolation,
    and integrates the ODE system numerically using solve_ivp.

    It verifies heat flux conservation between inner and outer boundaries and warns
    if the flux discrepancy exceeds the specified tolerance.

    Symmetry condition at r=0 is handled by setting the second derivative of temperature to zero.

    Warnings are issued if the ODE solver fails or if boundary fluxes are inconsistent.

    This method is suitable for modeling steady heat conduction in cylindrical coordinates
    with radial dependence and non-constant thermal conductivity.
    """

    r0, R = r
    T0, T1_input, Q = bc

    # Detect constant or interpolated k(T)
    if isinstance(k, (float, int)):
        k_const = float(k)
        def k_interp(T): return k_const
        def dk_interp(T): return 0.0
    else:
        k = np.asarray(k)
        k_interp = interp1d(k[:, 0], k[:, 1], kind='cubic', fill_value="extrapolate")
        T_fine = np.linspace(k[:, 0].min(), k[:, 0].max(), 1000)
        dk_dT_fine = np.gradient(k_interp(T_fine), T_fine)
        dk_interp = interp1d(T_fine, dk_dT_fine, kind='linear', fill_value="extrapolate")

    def area(r): return 2 * np.pi * r * L

    # Compute initial dT/dr with corrected minus sign
    if T1_input is None and Q is not None:
        A0 = area(r0)
        k0 = k_interp(T0)
        T1 = - Q / (k0 * A0)  # <- corrected minus sign
    elif Q is None and T1_input is not None:
        T1 = T1_input
    elif Q is not None and T1_input is not None:
        A0 = area(r0)
        k0 = k_interp(T0)
        expected_T1 = - Q / (k0 * A0)  # corrected minus sign
        if not np.isclose(T1_input, expected_T1, rtol=1e-4):
            raise ValueError("Inconsistent values: T'0 and Q do not satisfy dT/dr = -Q / (k(T) * A(r))")
        T1 = T1_input
    else:
        raise ValueError("Must provide either dT/dr or Q in bc")

    def system(r, y):
        T, dTdr = y
        k_val = k_interp(T)
        dk_dT_val = dk_interp(T)
        if r == 0:
            d2Tdr2 = 0  # symmetry condition
        else:
            d2Tdr2 = - (1 / k_val) * dk_dT_val * dTdr**2 - (1 / r) * dTdr
        return [dTdr, d2Tdr2]

    r_span = (r0, R)
    r_eval = np.linspace(r0, R, gridpoints)
    y0 = [T0, T1]

    sol = solve_ivp(system, r_span, y0, method=solver, t_eval=r_eval)

    if not sol.success:
        warnings.warn("ODE solver failed: " + sol.message)

    T_vals = sol.y[0]
    dTdr_vals = sol.y[1]
    r_vals = sol.t

    # Compute Q at r0 and r=R from numerical solution
    A_r0 = area(r0)
    k_r0 = k_interp(T_vals[0])
    Q_r0_calc = - k_r0 * A_r0 * dTdr_vals[0]

    A_R = area(R)
    k_R = k_interp(T_vals[-1])
    Q_R_calc = - k_R * A_R * dTdr_vals[-1]
    Q_error = Q_r0_calc - Q_R_calc

    # Check flux consistency
    if np.abs(Q_error) > tol * np.abs(Q_r0_calc):
        warnings.warn(f"Flux inconsistency: Q(r0)={Q_r0_calc:.4f}, Q(R)={Q_R_calc:.4f}")


    return {"r":        r_vals, 
            "T":        T_vals, 
            "dT/dr":    dTdr_vals,
            "Q_error":  Q_error}

def conduction_radial_analytical(
    radii,
    T_bounds,
    k_data_list,
    N_points_per_layer,
    L=1.0
):
    """
    Analytical solution for radial conduction in a multi-layered cylinder.

    Returns
    -------
    sol_guess : dict
        Dictionary with 'r', 'T', 'Q_dot', 'q_dot', and 'dT_dr'
    """
    n = len(k_data_list)
    T1, Tn1 = T_bounds

    # Compute average temperature per layer (linear interpolation in log space)
    ln_r = np.log(radii)
    T_interface = np.interp(ln_r, [ln_r[0], ln_r[-1]], [T1, Tn1])

    k_avgs = []
    for i in range(n):
        T_avg = 0.5 * (T_interface[i] + T_interface[i + 1])
        k_data = k_data_list[i]

        if np.isscalar(k_data):
            k_avg = float(k_data)
        else:
            T_vals, k_vals = k_data[:, 0], k_data[:, 1]
            k_interp = interp1d(T_vals, k_vals, kind='linear', fill_value='extrapolate')
            k_avg = float(k_interp(T_avg))

        k_avgs.append(k_avg)

    # Compute total thermal resistance and heat flow Q_dot
    resistances = [np.log(radii[i + 1] / radii[i]) / (2 * np.pi * L * k_avgs[i]) for i in range(n)]
    R_tot = sum(resistances)
    Q_dot = (T1 - Tn1) / R_tot

    # Build temperature profile T(r)
    r_all = []
    T_all = []
    k_all = []

    T_start = T1
    for i in range(n):
        r0, r1 = radii[i], radii[i + 1]
        k = k_avgs[i]
        N = N_points_per_layer[i]

        r_layer = np.linspace(r0, r1, N) if i == 0 else np.linspace(r0, r1, N)[1:]
        T_layer = T_start - (Q_dot / (2 * np.pi * L * k)) * np.log(r_layer / r0)
        T_start = T_layer[-1]

        r_all.append(r_layer)
        T_all.append(T_layer)
        k_all.append(np.full_like(r_layer, k))

    r_all = np.concatenate(r_all)
    T_all = np.concatenate(T_all)
    k_all = np.concatenate(k_all)

    def compute_gradients_per_layer_forward_diff(r_all, T_all, k_all, radii, N_points_per_layer):
        dT_dr = np.empty_like(T_all)
        q_dot = np.empty_like(T_all)
        
        start_idx = 0
        n_layers = len(N_points_per_layer)
        
        for i in range(n_layers):
            if i == 0:
                N = N_points_per_layer[i]
            else:
                N = N_points_per_layer[i] - 1  # skip overlapping first point
            
            end_idx = start_idx + N
            
            r_layer = r_all[start_idx:end_idx]
            T_layer = T_all[start_idx:end_idx]
            k_layer = k_all[start_idx:end_idx]
            
            # Forward difference for gradient
            dT_dr_layer = (T_layer[1:] - T_layer[:-1]) / (r_layer[1:] - r_layer[:-1])
            
            dT_dr_layer_full = np.empty(N)
            dT_dr_layer_full[:-1] = dT_dr_layer
            dT_dr_layer_full[-1] = dT_dr_layer[-1]
            
            dT_dr[start_idx:end_idx] = dT_dr_layer_full
            q_dot[start_idx:end_idx] = -k_layer * dT_dr_layer_full
            
            start_idx = end_idx
        
        return dT_dr, q_dot

    dT_dr, q_dot = compute_gradients_per_layer_forward_diff(r_all, T_all, k_all, radii, N_points_per_layer)

    sol_guess = {
        'r': r_all,
        'T': T_all,
        'Q_dot': Q_dot,
        'q_dot': q_dot,
        'dT_dr': dT_dr
    }
    return sol_guess

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # Common parameters
    Q = -17.11  # Negative for outward heat flow
    L = 92 / 1000
    gridpoints = 200

    # --- Layer 1 ---
    k1 = 0.2
    r1 = (55 / 1000, 60 / 1000)
    bc1 = [-130 + 273, None, Q]

    result1 = conduction_radial_steady_numerical(r1, L, bc1, k1, gridpoints)
    r_vals1 = result1["r"]
    T_vals1 = result1["T"]

    # --- Layer 2 ---
    k2 = 0.025
    r2 = (60 / 1000, 67 / 1000)
    T_interface_12 = T_vals1[-1]
    bc2 = [T_interface_12, None, Q]

    result2 = conduction_radial_steady_numerical(r2, L, bc2, k2, gridpoints)
    r_vals2 = result2["r"]
    T_vals2 = result2["T"]

    # --- Layer 3 ---
    k3 = 0.2
    r3 = (67 / 1000, 70 / 1000)
    T_interface_23 = T_vals2[-1]
    bc3 = [T_interface_23, None, Q]

    result3 = conduction_radial_steady_numerical(r3, L, bc3, k3, gridpoints)
    r_vals3 = result3["r"]
    T_vals3 = result3["T"]

    # --- Combine results ---
    r_total = np.concatenate([r_vals1, r_vals2, r_vals3])
    T_total = np.concatenate([T_vals1, T_vals2, T_vals3])

    # --- Plot temperature profile ---
    plt.plot(r_total, T_total, label="T(r) across 3-layer wall")
    plt.axvline(r1[1], color='gray', linestyle='--', linewidth=0.8, label='Interface 1–2')
    plt.axvline(r2[1], color='gray', linestyle='--', linewidth=0.8, label='Interface 2–3')

    # Mark and label boundary/interface temperatures
    boundary_radii = [r1[0], r1[1], r2[1], r3[1]]
    boundary_temps = [T_vals1[0], T_interface_12, T_interface_23, T_vals3[-1]]
    labels = ["r = 55 mm", "r = 60 mm", "r = 67 mm", "r = 70 mm"]

    plt.scatter(boundary_radii, boundary_temps, color='red', zorder=5)
    for r_pt, T_pt, label in zip(boundary_radii, boundary_temps, labels):
        plt.text(r_pt, T_pt + 2, f"{T_pt:.1f} K\n({label})", ha='center', va='bottom', fontsize=8, color='red')

    plt.xlabel("Radius r (m)")
    plt.ylabel("Temperature T (K)")
    plt.title("Radial Temperature Profile in Triple-Layered Wall")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__": 
    radii = [55/1000,60/1000,67/1000,70/1000]
    T_bounds = (-130+273, 20+273.0)
    L = 92/1000

    k1 = 0.2
    T_vals = np.linspace(300, 400, 5)
    k_vals = 10 + 0.05 * (T_vals - 300)
    k2 = np.column_stack((T_vals, k_vals))
    k2 = 0.025
    k3 = 0.2
    k_data_list = [k1, k2, k3]
    N_points = [300, 400, 300]

    sol_guess = conduction_radial_analytical(radii, T_bounds, k_data_list, N_points, L=L)

    r = sol_guess['r']
    T = sol_guess['T']
    q_dot = sol_guess['q_dot']
    dT_dr = sol_guess['dT_dr']
    Q_dot = sol_guess['Q_dot']

    fig, ax1 = plt.subplots(figsize=(9, 5))

    ax1.plot(r * 1000, T, 'tab:blue', label='Temperature (K)')
    ax1.set_xlabel('Radius (mm)')
    ax1.set_ylabel('Temperature (K)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    for ri in radii:
        ax1.axvline(ri * 1000, color='gray', linestyle=':', linewidth=1)
        idx = (np.abs(r - ri)).argmin()
        T_ri = T[idx]
        ax1.text(ri * 1000, T_ri + 5, f"{T_ri:.1f} K", ha='center', va='bottom', fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(r * 1000, q_dot, 'tab:red', label='Heat Flux (W/m²)', linestyle='--')
    ax2.set_ylabel('Heat Flux (W/m²)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f"Radial Temperature & Heat Flux | Q = {Q_dot:.2f} W")
    fig.tight_layout()
    plt.grid(True)
    plt.show()