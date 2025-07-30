from .math_utils import safe_divide
from .general_utils import validate_inputs

def mass_leakrate(*, mode="Mode 1", M=None, V=None, R=8.31446261815324, T=None, P=None, dPdt=None, dTdt=None, dRhodt=None, dRhodP=None, dRhodT=None, m=None, Rspecific=None):
    """
    Calculate mass leak rate (kg/s) from pressure change in an isochoric system with four modes.

    Modes and formulas:
        Mode 1:  m_dot = M * V / (R * T) * dP/dt                                (based on molar mass, moles)
        Mode 2:  m_dot = V * M / (R * T) * dRho/dt                              (based on density change)
        Mode 3:  m_dot = m / P * dP/dt                                          (relative pressure change)
        Mode 4:  m_dot = V / (Rspecific * T) * dP/dt                            (using specific gas constant)
        Mode 5:  m_dot = V * ( dRho/dt - dRho/dP|T dP/dt - dRho/dT|P dT/dt )    (Real gas)

    Parameters:
        mode : str, optional
            "Mode 1", "Mode 2", "Mode 3", or "Mode 4"
        M : float
            Molar mass (kg/mol)
        V : float
            Volume (m^3)
        R : float
            Universal gas constant (J/(mol·K))
        T : float
            Temperature (K)
        P : float
            Pressure (Pa)
        dPdt : array
            Pressure time derivative (Pa/s)
        dTdt : array
            Temperature time derivative (K/s)
        dRhodt : array
            Density time derivative (kg/m^3/s)
        dRhodP : array
            Density pressure derivative at constant temperature (kg/m^3Pa)
        dRhodT : array
            Density Temperature derivative at constant pressure (kg/m^3K)
        m : float
            Current mass (kg)
        Rspecific : float
            Specific gas constant (J/(kg·K))
        

    Returns:
        m_dot : float or ndarray
            Mass leak rate in kg/s.

    Raises:
        ValueError: if required parameters are missing or mode is invalid.
    """
    if mode == "Mode 1":
        if M is None or V is None or R is None or T is None or dPdt is None:
            raise ValueError("Mode 1 requires M, V, R, T, and dPdt")
        dPdt = validate_inputs(dPdt)
        M, V, R, T = validate_inputs(M, V, R, T, allow_array=False)
        dPdt, M, V, R, T = validate_inputs(dPdt, M, V, R, T, check_broadcast=True)
        return M * V / (R * T) * dPdt

    elif mode == "Mode 2":
        if V is None or M is None or R is None or T is None or dRhodt is None:
            raise ValueError("Mode 2 requires V, M, R, T, and dRhodt")
        dRhodt = validate_inputs(dRhodt)
        V, M, R, T = validate_inputs(V, M, R, T, allow_array=False)
        dRhodt, V, M, R, T = validate_inputs(dRhodt, V, M, R, T, check_broadcast=True)
        return V * M / (R * T) * dRhodt

    elif mode == "Mode 3":
        if m is None or P is None or dPdt is None:
            raise ValueError("Mode 3 requires m, P, and dPdt")
        dPdt = validate_inputs(dPdt)
        m, P = validate_inputs(m, P, allow_array=False)
        dPdt, m, P = validate_inputs(dPdt, m, P, check_broadcast=True)
        return safe_divide(m, P) * dPdt

    elif mode == "Mode 4":
        if V is None or Rspecific is None or T is None or dPdt is None:
            raise ValueError("Mode 4 requires V, Rspecific, T, and dPdt")
        dPdt = validate_inputs(dPdt)
        V, Rspecific, T = validate_inputs(V, Rspecific, T, allow_array=False)
        dPdt, V, Rspecific, T = validate_inputs(dPdt, V, Rspecific, T, check_broadcast=True)
        return V / (Rspecific * T) * dPdt
    
    elif mode == "Mode 5":
        if V is None or dRhodt is None or dRhodP is None or dRhodT is None or dPdt is None or dTdt is None:
            raise ValueError("Mode 4 requires V, dRhodt, dRhodP, dRhodT, dPdt and dTdt")
        dRhodt, dRhodP, dRhodT, dPdt, dTdt = validate_inputs(dRhodt, dRhodP, dRhodT, dPdt, dTdt)
        V = validate_inputs(V, allow_array=False)


    else:
        raise ValueError("Invalid mode. Choose 'Mode 1', 'Mode 2', 'Mode 3', 'mode4', or 'Mode 5'.")


if __name__ == "__main__":
    import numpy as np

    # Example inputs
    M = 0.02897          # molar mass of air in kg/mol
    V = 1e-3             # volume in m^3 (1 L)
    T = 300.0            # temperature in K
    P = 101325.0         # pressure in Pa (1 atm)
    m = 1.2e-3           # mass in kg (approximate air mass in 1L at STP)
    Rspecific = 287.0    # specific gas constant for air in J/(kg·K)
    
    # Time derivative arrays (simulated)
    dPdt = np.array([-10, -20, -15, -5])       # pressure drop rate in Pa/s
    dRhodt = np.array([-0.01, -0.02, -0.015, -0.005])  # density change rate in kg/m³/s

    print("Mode 1 mass leak rate:", mass_leakrate(mode="Mode 1", M=M, V=V, T=T, P=P, dPdt=dPdt))
    print("Mode 2 mass leak rate:", mass_leakrate(mode="Mode 2", M=M, V=V, T=T, P=P, dRhodt=dRhodt))
    print("Mode 3 mass leak rate:", mass_leakrate(mode="Mode 3", m=m, P=P, dPdt=dPdt))
    print("Mode 4 mass leak rate:", mass_leakrate(mode="Mode 4", V=V, Rspecific=Rspecific, T=T, dPdt=dPdt))
