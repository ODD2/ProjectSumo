"""
od/engine.py - MATLAB engine interface and PHY-layer lookup tables.

Manages the lifecycle of the shared MATLAB engine process and exposes
helper functions for CQI selection and per-resource-block throughput
calculation.  The engine is started once per simulation run and all MATLAB
script directories are added to its path automatically.
"""
import matlab.engine
import os
# Simulation Independent Variables
MATLAB_ENG = None


def InitializeSimulationContext(interest_config):
    """Start the MATLAB engine and set up simulation context for a run.

    Starts the engine if it is not already running, adds all MATLAB script
    directories to the engine path, and calls the MATLAB-side
    InitializeSimulationContext to seed the RNG.

    Args:
        interest_config: InterestConfig whose rng_seed is forwarded to MATLAB.
    """
    global MATLAB_ENG
    if(MATLAB_ENG == None):
        MATLAB_ENG = matlab.engine.start_matlab()
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/")
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/SelectCQI_bySNR/")
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/PlannerV1/")
        MATLAB_ENG.InitializeSimulationContext(int(interest_config.rng_seed), nargout=0)


def TerminateMatlabEngine():
    """Quit the MATLAB engine process if it is running."""
    global MATLAB_ENG
    if(not MATLAB_ENG == None):
        MATLAB_ENG.quit()


# Minimum SINR threshold (dB) required to achieve each CQI index (0–15).
# Index 0 represents an out-of-range condition (SINR = -inf).
# Values follow 3GPP TS 36.213 Table 7.2.3-1 at 10% BLER.
CQI_SINR = [
    float("-inf"),
    -6.9,
    -5.1,
    -3.1,
    -1.4,
    0.80,
    2.60,
    4.70,
    6.50,
    8.40,
    10.40,
    12.30,
    14.10,
    15.90,
    17.75,
    19.70
]


def SelectCQI_BLER10P(SINR):
    """Return the highest CQI index whose SINR threshold does not exceed *SINR*.

    Uses the 10 % BLER operating point defined in CQI_SINR.

    Args:
        SINR: Received SINR value in dB.

    Returns:
        Integer CQI index in [0, 15].  Returns 0 when SINR is below the
        lowest threshold (out-of-range).
    """
    for i in range(0, len(CQI_SINR), 1):
        if(SINR < CQI_SINR[i]):
            return i - 1
    else:
        return i


# Spectral efficiency (bits per subcarrier per symbol) for each CQI index.
# Each value represents the code rate × modulation order product for the
# corresponding MCS, used to compute throughput per resource block.
RB_EFFICIENCY = [
    0,
    0.1523,
    0.2344,
    0.3770,
    0.6016,
    0.8770,
    1.1758,
    1.4766,
    1.9141,
    2.4063,
    2.7305,
    3.3223,
    3.9023,
    4.5234,
    5.1152,
    5.5547
]


def GetThroughputPerRB(CQI, SymbolPerSlot):
    """Calculate the number of bits a single resource block can carry.

    A resource block spans 12 subcarriers × SymbolPerSlot OFDM symbols.
    The bit-load per subcarrier-symbol is given by RB_EFFICIENCY[CQI].

    Args:
        CQI:          CQI index (0–15).
        SymbolPerSlot: Number of OFDM symbols in one slot (e.g. 14 for normal CP).

    Returns:
        Integer number of bits deliverable by one RB under the given CQI.
    """
    CQI = int(CQI)
    SymbolPerSlot = int(SymbolPerSlot)
    return round(12.0 * SymbolPerSlot * RB_EFFICIENCY[CQI])
